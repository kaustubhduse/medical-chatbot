# similarity.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ReportComparator:
    def __init__(self, vectorstore):
        """Initialize with a vectorstore containing embeddings and reports"""
        self.vectorstore = vectorstore

    def find_similar_reports(self, embedding, k=5):
        """Find top-k similar reports based on cosine similarity"""
        # Get all embeddings from vectorstore
        all_embeddings = self.vectorstore.get_vectors()  # Assumes this method exists
        if all_embeddings is None or len(all_embeddings) == 0:
            return []

        # Compute cosine similarity
        similarities = cosine_similarity([embedding], all_embeddings)[0]

        # Get indices of top-k similar reports (highest similarity first)
        top_indices = np.argsort(similarities)[::-1][:k]

        # Retrieve corresponding reports or metadata
        similar_reports = [self.vectorstore.get_report(i) for i in top_indices]  # Assumes get_report method

        # Return list of (report, similarity_score)
        return [(similar_reports[i], similarities[top_indices[i]]) for i in range(len(top_indices))]

    def add_report(self, embedding, report_metadata):
        """Add a new report embedding and metadata to the vectorstore"""
        self.vectorstore.add(embedding, report_metadata)
