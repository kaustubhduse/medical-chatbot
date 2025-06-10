import numpy as np
import uuid
from langchain_community.vectorstores import FAISS

class ReportComparator:
    def __init__(self, vectorstore):
        """Initialize with LangChain FAISS vectorstore"""
        self.vectorstore = vectorstore

    def find_similar_reports(self, embedding, k=5):
        """Find similar reports using FAISS built-in methods"""
        try:
            # Convert to numpy array
            query_embedding = np.array(embedding, dtype=np.float32)
            
            # Use FAISS's native similarity search
            docs_and_scores = self.vectorstore.similarity_search_by_vector(
                query_embedding.flatten().tolist(), 
                k=k
            )
            
            return [(doc.metadata, 1) for doc, _ in docs_and_scores]  # 1 = max similarity
            
        except Exception as e:
            print(f"Similarity search error: {str(e)}")
            return []

    def add_report(self, text, metadata):
        """Add new report using proper LangChain API"""
        self.vectorstore.add_texts(
            texts=[text],
            metadatas=[metadata],
            ids=[metadata.get('id', str(uuid.uuid4()))]
        )
