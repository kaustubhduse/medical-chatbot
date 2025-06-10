# similarity.py
import numpy as np

class ReportComparator:
    def __init__(self, vectorstore):
        """Initialize with a LangChain FAISS vectorstore"""
        self.vectorstore = vectorstore
        self.index = vectorstore.index  # Direct access to FAISS index
        self.docstore = vectorstore.docstore

    def find_similar_reports(self, embedding, k=5):
        """Find top-k similar reports using FAISS native search"""
        # Convert to numpy array with proper dtype
        query_embedding = np.array([embedding], dtype=np.float32)
        
        # Search FAISS index
        distances, indices = self.index.search(query_embedding, k)
        
        # Retrieve documents from docstore
        similar_docs = []
        for idx in indices[0]:
            if idx in self.vectorstore.index_to_docstore_id:
                doc_id = self.vectorstore.index_to_docstore_id[idx]
                doc = self.docstore.search(doc_id)
                similar_docs.append((doc, 1 - distances[0][0]))  # Convert distance to similarity
        
        return similar_docs

    def add_report(self, embedding, report_metadata):
        """Add a new report to the vectorstore"""
        # Convert to numpy array with proper dtype
        embedding_array = np.array([embedding], dtype=np.float32)
        
        # Use LangChain's add_embeddings method
        self.vectorstore.add_embeddings(
            text_embeddings=[(report_metadata['content'], embedding_array[0])],
            metadatas=[report_metadata],
            ids=[report_metadata['id']]
        )
