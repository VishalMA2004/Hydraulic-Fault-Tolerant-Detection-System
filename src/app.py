import streamlit as st
import sys
import os

# Ensure src directory is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_ingestion import DataIngestionPipeline
from src.rag_engine import RAGEngine
from src.main import MockHydraulicLLM

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
    
    if st.button("Run Data Ingestion"):
        with st.spinner("Ingesting documents..."):
            try:
                ingestion = DataIngestionPipeline()
                ingestion.run()
                st.success("✅ Data Ingestion Complete!")
            except Exception as e:
                st.error(f"Error during ingestion: {e}")

# Main Chat Interface
input_symptom = st.text_area("Descolibe the hydraulic symptom:", height=100, placeholder="e.g., Pump is making cavitating noise and system pressure is fluctuating...")

if st.button("🔍 Diagnose Fault", type="primary"):
    if not input_symptom:
        st.warning("Please enter a symptom first.")
    else:
        with st.spinner("Analyzing technical manuals..."):
            try:
                # Initialize RAG Engine
                # In production, replace MockHydraulicLLM with actual loading logic
                llm = MockHydraulicLLM() 
                rag = RAGEngine(llm_inference=llm)
                
                response = rag.predict(input_symptom)
                
                st.subheader("📋 Diagnostic Report")
                st.markdown(response)
                
            except FileNotFoundError:
                st.error("🚨 Vector Store not found! Please run 'Data Ingestion' from the sidebar first.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Powered by RAG + Fine-Tuned LLM | Sources: OEM Technical Manuals")
