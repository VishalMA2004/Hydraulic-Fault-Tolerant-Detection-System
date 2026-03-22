import streamlit as st
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_ingestion import DataIngestionPipeline
from rag_engine import RAGEngine
from main import MockHydraulicLLM, GeminiHydraulicLLM
from dotenv import load_dotenv

load_dotenv()

# Page Config
st.set_page_config(
    page_title="Hydraulic Fault Predictor",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Intelligent Hydraulic Fault Prediction System")
st.markdown("### Diagnosis & Mitigation using RAG + Fine-Tuned LLM")

# Sidebar for Admin/Ingestion
with st.sidebar:
    st.header("⚙️ Data Management")
    st.info("Place PDF manuals in `data/pdfs/` before running ingestion.")
    
    api_key_input = st.text_input(
        "Gemini API Key", 
        type="password", 
        help="Enter your Google Gemini API Key. Leave this blank if using a .env file."
    )
    
    if st.button("Run Data Ingestion"):
        with st.spinner("Ingesting documents..."):
            try:
                ingestion = DataIngestionPipeline()
                ingestion.run()
                st.success("✅ Data Ingestion Complete!")
            except Exception as e:
                st.error(f"Error during ingestion: {e}")

# Main Chat Interface
input_symptom = st.text_area(
    "Describe the hydraulic symptom:",
    height=100,
    placeholder="e.g., Pump is making cavitating noise and system pressure is fluctuating..."
)

if st.button("🔍 Diagnose Fault", type="primary"):
    if not input_symptom:
        st.warning("Please enter a symptom first.")
    else:
        with st.spinner("Analyzing technical manuals..."):
            try:
                # Initialize RAG Engine
                llm_key = api_key_input or os.environ.get("GEMINI_API_KEY")
                if not llm_key:
                    st.warning("No Gemini API Key provided. Falling back to Mock LLM.")
                    llm = MockHydraulicLLM()
                else:
                    llm = GeminiHydraulicLLM(api_key=llm_key)
                
                rag = RAGEngine(llm_inference=llm)
                
                response = rag.predict(input_symptom)
                
                st.subheader("📋 Diagnostic Report")
                st.markdown(response)
                
            except FileNotFoundError as e:
                st.error("🚨 Vector Store not found! Please run 'Data Ingestion' from the sidebar first.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Powered by RAG + Fine-Tuned LLM | Sources: OEM Technical Manuals")
