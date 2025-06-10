import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

import os
from data_analysis.data_analysis import (
    parse_llm_summary,
    display_metric_summary,
    predict_conditions,
    download_metrics
)

# Load environment variables
load_dotenv()


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    if not text.strip():
        st.error("⚠️ No readable text found in uploaded PDFs! Please ensure they contain selectable text.")
        return None
    return text


def summarize_text(text):
    try:
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            st.error("❌ API key missing! Please set TOGETHER_API_KEY in your environment variables.")
            return None

        llm = ChatOpenAI(
            base_url="https://api.together.xyz/v1",
            api_key=api_key,
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        )

        summary_prompt = (
            "You are a medical expert assistant. Carefully read and summarize the following medical report. "
            "Your summary should include:\n"
            "- Patient's name (if available)\n"
            "- Date of the report (if available)\n"
            "- Relevant medical history or background (in bullet points)\n"
            "- Key findings and observations (in bullet points)\n"
            "- Diagnoses or impressions (if mentioned)\n"
            "- Recommendations for further tests, treatments, or follow-up (in bullet points)\n"
            "\n"
            "Write the summary in clear, plain language that is understandable to both medical professionals and patients. "
            "Read the following medical report. For each test, output a JSON object with these fields: "
            "'metric', 'value', 'reference_range', and 'status' (Low/Normal/High). "
            "If any field is missing, use null. Output only a JSON array. \n\n"
            f"{text}"
        )
        summary = llm.predict(summary_prompt)
        return summary
    except Exception as e:
        st.error(f"❌ Error generating summary: {e}")
        return None


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    if not chunks:
        st.error("⚠️ No valid text chunks found! Ensure PDFs contain readable text.")
        return None
    return chunks


def get_vectorstore(text_chunks):
    if not text_chunks:
        raise ValueError("Error: No text chunks provided for FAISS indexing!")

    model_name = "sentence-transformers/all-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    try:
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            st.error("❌ API key missing! Please set TOGETHER_API_KEY in your environment variables.")
            return None

        llm = ChatOpenAI(
            base_url="https://api.together.xyz/v1",
            api_key=api_key,
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        )

        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
        return conversation_chain
    except Exception as e:
        st.error(f"❌ Error initializing chat: {e}")
        return None


def handle_userinput(user_question):
    if st.session_state.conversation:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']

        for i, message in enumerate(st.session_state.chat_history):
            role = "User" if i % 2 == 0 else "Bot"
            st.write(f"**{role}:** {message.content}")
    else:
        st.warning("⚠️ No conversation started yet! Upload PDFs and process them first.")


def main():
    st.set_page_config(page_title="Medical Chatbot", page_icon="⚕️")

    for key in ["conversation", "chat_history", "pdf_text", "text_chunks", "vectorstore", "summary"]:
        if key not in st.session_state:
            st.session_state[key] = None

    st.header("⚕️ Chat with Medical Reports")

    user_question = st.text_input("Ask a question about your medical report:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("📄 Upload Medical Reports (PDF)")
        pdf_docs = st.file_uploader("Upload PDFs and click 'Process'", accept_multiple_files=True)

        if st.button("🚀 Process"):
            with st.spinner("⏳ Processing..."):
                if not pdf_docs:
                    st.error("⚠️ Please upload at least one PDF file!")
                    return

                raw_text = get_pdf_text(pdf_docs)
                if not raw_text:
                    return

                st.session_state.pdf_text = raw_text

                # Generate summary but DO NOT display it
                summary = summarize_text(raw_text)
                if summary:
                    st.session_state.summary = summary
                    st.download_button(
                        "📥 Download Medical Summary", 
                        summary.encode('utf-8'), 
                        file_name="medical_summary.txt", 
                        mime="text/plain"
                    )

                # Extract health metrics and display
                parsed_data = parse_llm_summary(summary)
                display_metric_summary(parsed_data)
                predict_conditions(parsed_data)
                download_metrics(parsed_data)

                # Text chunking + vectorstore + conversation setup
                text_chunks = get_text_chunks(raw_text)
                if not text_chunks:
                    return

                st.session_state.text_chunks = text_chunks

                try:
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.vectorstore = vectorstore
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    st.success("✅ Processing complete! You can now ask questions.")
                except ValueError as e:
                    st.error(f"❌ Error: {e}")



if __name__ == '__main__':
    main()
