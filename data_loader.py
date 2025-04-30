from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

# This class handles loading and preprocessing of text documents
class DataLoader():
    def __init__(self, dir_path) -> None:
        # Path to the directory containing .txt documents
        self.dir_path = dir_path
        # Load all documents upon initialization
        self.docs = self._load_document()

    def _load_document(self) -> List:
        # DirectoryLoader recursively loads all .txt files
        dir_loader = DirectoryLoader(self.dir_path, glob='**/*.txt', loader_cls=TextLoader)
        docs = dir_loader.load()
        return docs
        
    def chunk_docs(self):
        # Split documents into 500-character chunks with 200-character overlap
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
        chunk_documents = text_splitter.transform_documents(self.docs)
        return chunk_documents
    
