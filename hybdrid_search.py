from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# This class builds a hybrid retriever using both keyword and semantic search
class HybridRetriever():
    def  __init__(self, docs) -> None:
        self.docs = docs
        # Use HuggingFace sentence-transformer model for semantic embeddings
        self.model_name = "sentence-transformers/all-mpnet-base-v2"
        self.model_kwargs = {"device":"cpu"}
        self.encode_kwargs = {'normalize_embeddings': False}

    # Create keyword-based search using BM25 algorithm
    def _create_keyword_search(self):
        bm25_retriever = BM25Retriever.from_documents(
            self.docs       
        )
        bm25_retriever.k = 3 # Return top 3 relevant documents
        return bm25_retriever
    
    # Create semantic search using HuggingFace embeddings + FAISS
    def _create_semantic_search(self):
        hf_embedding = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs=self.model_kwargs,
            encode_kwargs=self.encode_kwargs
        )
        # Use FAISS as vector store to index documents
        faiss_vectorstore = FAISS.from_documents(self.docs, hf_embedding)
        faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": 3})
        return faiss_retriever
    
    # Combine both keyword and semantic retrievers using weighted ensemble
    def create_hybrid_search(self):
        ensemble_retriever = EnsembleRetriever(
            retrievers=[self._create_keyword_search(), self._create_semantic_search()], weight=[0.6, 0.4] # 60% keyword, 40% semantic
        )
        return ensemble_retriever
