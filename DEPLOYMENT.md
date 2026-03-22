# 🔧 Intelligent Hydraulic Fault Prediction System - Streamlit Deployment Guide

## Local Deployment

### Prerequisites
- Python 3.8+
- pip or conda

### Setup Instructions

1. **Clone/Navigate to the project directory:**
   ```bash
   cd "v:\Anti\Project Tha"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare your data:**
   - Place PDF manuals in the `data/pdfs/` directory
   - Run data ingestion through the Streamlit app sidebar, or run directly:
     ```bash
     python src/data_ingestion.py
     ```

5. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

   The app will open at `http://localhost:8501`

---

## Deployment to Streamlit Cloud

### Prerequisites
- GitHub account with the project repository
- Streamlit Community Cloud account (https://streamlit.io/cloud)

### Steps

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repo, branch, and main file: `streamlit_app.py`
   - Click "Deploy"

3. **Managing PDF files:**
   - For production, store PDFs in a cloud storage (AWS S3, Azure Blob, etc.)
   - Update `data_ingestion.py` to download PDFs from cloud storage
   - Or, have users upload PDFs through the Streamlit interface (add file uploader)

### Requirements for Cloud Deployment
- Ensure `requirements.txt` has all dependencies pinned to versions
- Keep the project structure intact
- Make sure PDFs are accessible (upload to repo or use cloud storage)

---

## Project Structure

```
├── streamlit_app.py          # Main Streamlit app entry point
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── src/
│   ├── app.py               # Original Streamlit app (legacy)
│   ├── main.py              # Mock LLM and main logic
│   ├── rag_engine.py        # RAG pipeline
│   ├── data_ingestion.py    # PDF processing & vector store creation
│   └── prompts.py           # Prompt templates
├── data/
│   ├── pdfs/                # Place PDF manuals here
│   └── vector_store/        # Generated FAISS index (auto-created)
└── docs/
    └── Project_Report.md    # Project documentation
```

---

## Troubleshooting

### "Vector Store not found" error
- Click "Run Data Ingestion" in the sidebar
- Ensure PDFs are in `data/pdfs/` directory
- Wait for processing to complete

### Dependencies not installing
- Try: `pip install --upgrade pip`
- Then: `pip install -r requirements.txt`

### Path errors on different OS
- The code uses `os.path.join()` for cross-platform compatibility
- Should work on Windows, macOS, and Linux

---

## Features

✅ **PDF Ingestion** - Loads and processes OEM technical manuals  
✅ **Vector Embeddings** - Uses HuggingFace embeddings for semantic search  
✅ **RAG Pipeline** - Retrieves relevant context from manuals  
✅ **Mock LLM** - Demonstrates the system with mocked responses  
✅ **Streamlit UI** - Professional, user-friendly interface  

---

## Next Steps

1. Replace `MockHydraulicLLM` with a real LLM (Ollama, OpenAI, Hugging Face, etc.)
2. Add file upload functionality for PDFs
3. Implement caching for vector store
4. Add authentication if deploying as a service
5. Set up monitoring and logging

---

## Support

For issues or questions, refer to:
- [Streamlit Docs](https://docs.streamlit.io/)
- [LangChain Docs](https://python.langchain.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)
