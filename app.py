import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import os
import speech_recognition as sr
import pyttsx3
import threading
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# Load environment variables
load_dotenv()

# Initialize text-to-speech engine once
if "engine" not in st.session_state:
    st.session_state.engine = pyttsx3.init()

# Function to convert text to speech in a separate thread
def speak(text):
    def run_speech():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    
    threading.Thread(target=run_speech).start()
    
# Function to capture voice input and convert it to text
def get_voice_input():
    st.write("🎤 Listening... Speak now!")
    
    # Set recording parameters
    duration = 5  # Maximum recording duration in seconds
    sample_rate = 16000  # Sample rate for audio recording
    
    try:
        # Record audio
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        
        # Save the recorded audio to a temporary file
        temp_file = "temp.wav"
        wav.write(temp_file, sample_rate, audio)
        
        # Use speech_recognition to convert audio to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            st.write(f"👤 You said: {text}")
            return text
    except sr.UnknownValueError:
        st.error("❌ Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        st.error("❌ Speech recognition service is down. Please try again later.")
        return None
    except Exception as e:
        st.error(f"❌ Error during recording: {e}")
        return None

    
# Function to extract text from PDFs
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

# Function to summarize medical reports using AI
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
            "Summarize the following medical report in a clear and concise manner. "
            "Give the name of the patient, date of report, and any relevant medical history in points. "
            "Highlight key observations, diagnoses, and recommendations. "
            "Ensure the summary is understandable for both medical professionals and patients.\n\n"
            f"{text}"
        )
        
        summary = llm.predict(summary_prompt)
        
         # Correct file path inside the client-side public directory
        base_dir = os.path.abspath("client/client-side/public")
        summary_file_path = os.path.join(base_dir, "summary.txt")

        # Ensure directory exists
        os.makedirs(base_dir, exist_ok=True)
        
        # Save the summary to a text file
        with open(summary_file_path, "w", encoding="utf-8") as file:
            file.write(summary)

        return "/summary.txt"  # Return the relative public path
    except Exception as e:
        st.error(f"❌ Error generating summary: {e}")
        return None

# Function to split text into chunks
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

# Function to create a vector store
def get_vectorstore(text_chunks):
    if not text_chunks:
        raise ValueError("Error: No text chunks provided for FAISS indexing!")
    
    model_name = "sentence-transformers/all-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Function to create a conversation chain
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

# Function to handle user input in chatbot
def handle_userinput(user_question):
    if st.session_state.conversation:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']
        
        for i, message in enumerate(st.session_state.chat_history):
            role = "User" if i % 2 == 0 else "Bot"
            st.write(f"**{role}:** {message.content}")
            if role == "Bot":
                speak(message.content)  # Speak the bot's response
    else:
        st.warning("⚠️ No conversation started yet! Upload PDFs and process them first.")

# Main function
def main():
    st.set_page_config(page_title="Medical Chatbot", page_icon="⚕️")
    
    # Initialize session state variables
    for key in ["conversation", "chat_history", "pdf_text", "text_chunks", "vectorstore", "summary"]:
        if key not in st.session_state:
            st.session_state[key] = None

    st.header("⚕️ Chat with Medical Reports")
    
    # User input box for chat
    user_question = st.text_input("Ask a question about your medical report:")
    if user_question:
        handle_userinput(user_question)

    # Voice input button
    if st.button("🎤 Use Voice Input"):
        voice_input = get_voice_input()
        if voice_input:
            handle_userinput(voice_input)

    with st.sidebar:
        st.subheader("📄 Upload Medical Reports (PDF)")
        pdf_docs = st.file_uploader("Upload PDFs and click 'Process'", accept_multiple_files=True)
        
        if st.button("🚀 Process"):
            with st.spinner("⏳ Processing..."):
                if not pdf_docs:
                    st.error("⚠️ Please upload at least one PDF file!")
                    return
                
                # Extract text from PDFs
                raw_text = get_pdf_text(pdf_docs)
                if not raw_text:
                    return
                
                st.session_state.pdf_text = raw_text

                # Generate medical summary
                summary = summarize_text(raw_text)
                if summary:
                    st.session_state.summary = summary
                    st.success("✅ Summary generated!")

                # Process text into chunks
                text_chunks = get_text_chunks(raw_text)
                if not text_chunks:
                    return
                
                st.session_state.text_chunks = text_chunks

                # Create vector store & initialize chat
                try:
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.vectorstore = vectorstore
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    st.success("✅ Processing complete! You can now ask questions.")
                except ValueError as e:
                    st.error(f"❌ Error: {e}")

if __name__ == '__main__':
    main()  
