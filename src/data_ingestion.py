import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Configuration
import os
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(_ROOT, "data", "pdfs")
VECTOR_DB_PATH = os.path.join(_ROOT, "data", "vector_store")
EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

class DataIngestionPipeline:
    def __init__(self):
        print("Initializing Embedding Model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={'device': 'cpu'}, # Use 'cuda' if GPU is available
            encode_kwargs={'normalize_embeddings': True}
        )

    def load_documents(self, source_dir: str) -> List[Document]:
        """Loads all PDF documents from the specified directory."""
        documents = []
        if not os.path.exists(source_dir):
            os.makedirs(source_dir)
            print(f"Directory {source_dir} created. Please add PDF manuals there.")
            return []

        for filename in os.listdir(source_dir):
            if filename.endswith(".pdf"):
                file_path = os.path.join(source_dir, filename)
                print(f"Loading {file_path}...")
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                # Add source metadata
                for doc in docs:
                    doc.metadata['source_book'] = filename
                documents.extend(docs)
        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Splits documents into smaller chunks for embedding."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} pages into {len(chunks)} chunks.")
        return chunks

    def create_vector_store(self, chunks: List[Document]):
        """Generates embeddings and saves the vector store locally."""
        if not chunks:
            print("No chunks to process.")
            return

        print("Creating Vector Store (this may take time)...")
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        vector_store.save_local(VECTOR_DB_PATH)
        print(f"Vector store saved to {VECTOR_DB_PATH}")

    def run(self):
        print("Starting Data Ingestion Pipeline...")
        raw_docs = self.load_documents(DATA_DIR)
        if raw_docs:
            chunks = self.split_documents(raw_docs)
            self.create_vector_store(chunks)
            print("Data Ingestion Complete.")
        else:
            print("Skipping Vector Store creation (No documents found).")

if __name__ == "__main__":
    pipeline = DataIngestionPipeline()
    pipeline.run()
