import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
# In a real scenario with a local LLM, we'd import something like LlamaCpp or HuggingFacePipeline
# For this template, we will simulate the LLM interface or use a placeholder if the package isn't installed.
# We will assume a standard LangChain LLM interface.

from prompts import get_rag_prompt_template

VECTOR_DB_PATH = "../data/vector_store"
EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"

class RAGEngine:
    def __init__(self, llm_inference):
        """
        Args:
            llm_inference: An instance of a LangChain compatible LLM (e.g., LlamaCpp)
        """
        self.llm = llm_inference
        self.vector_store = self._load_vector_store()
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3} # Retrieve top 3 chunks
        )
        self.prompt = get_rag_prompt_template()

    def _load_vector_store(self):
        print("Loading Vector Store...")
        if not os.path.exists(VECTOR_DB_PATH):
            raise FileNotFoundError(f"Vector store not found at {VECTOR_DB_PATH}. Run data_ingestion.py first.")
        
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        return FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)

    def format_docs(self, docs):
        """Formats retrieved documents into a single string with source citation."""
        formatted_text = ""
        for i, doc in enumerate(docs):
            source = doc.metadata.get('source_book', 'Unknown Source')
            page = doc.metadata.get('page', 'N/A')
            formatted_text += f"\n[Source: {source}, Page: {page}]\n{doc.page_content}\n"
        return formatted_text

    def get_chain(self):
        """Returns the RAG execution chain."""
        return (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def predict(self, symptom: str):
        chain = self.get_chain()
        print(f"Analyzing symptom: {symptom}...")
        response = chain.invoke(symptom)
        return response
