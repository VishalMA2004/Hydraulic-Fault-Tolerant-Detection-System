import argparse
import sys
import os
from typing import Any, List, Optional
from pydantic import Field
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun

# Mocking LLM for demonstration if actual model is not present
# In production, use: from langchain_community.llms import LlamaCpp

class GeminiHydraulicLLM(LLM):
    """A wrapper for google-genai SDK to be used in LangChain."""
    api_key: Optional[str] = Field(default=None)

    @property
    def _llm_type(self) -> str:
        return "gemini_hydraulic_expert"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        from google import genai
        # Initialize client here to avoid pickling/threading issues and use the latest api_key
        key = self.api_key or os.environ.get("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY must be provided")
            
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text

class MockHydraulicLLM(LLM):
    """A Mock LLM to demonstrate the pipeline without a heavy local model."""
    @property
    def _llm_type(self) -> str:
        return "mock_hydraulic_expert"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        return f"""[MOCKED RESPONSE]
Based on the provided context, the issue '{{System Pressure Low}}' is likely caused by:
1. Worn pump internals (Source: Pump_Manual.pdf, Pg 45)
2. Relief valve setting too low.

Recommended Action:
1. Verify pump output flow.
2. Adjust relief valve to 200 bar as per specification.
"""

def main():
    parser = argparse.ArgumentParser(description="Hydraulic Fault Prediction System")
    parser.add_argument("--symptom", type=str, help="The observed hydraulic symptom", required=False)
    parser.add_argument("--ingest", action="store_true", help="Run data ingestion pipeline")
    args = parser.parse_args()

    # Step 1: Data Ingestion (Optional)
    if args.ingest:
        from data_ingestion import DataIngestionPipeline
        ingestion = DataIngestionPipeline()
        ingestion.run()
        print("Ingestion finished. Exiting.")
        return

    # Step 2: Inference
    if not args.symptom:
        print("Please provide a symptom using --symptom or run with --ingest to process data.")
        sys.exit(1)

    try:
        from rag_engine import RAGEngine
        
        # NOTE: Replace MockHydraulicLLM with your actual fine-tuned model
        # example: llm = LlamaCpp(model_path="path/to/finetuned-llama3.gguf", ...)
        # Using Gemini instead of Mock
        if not os.environ.get("GEMINI_API_KEY"):
            print("WARNING: GEMINI_API_KEY not found in environment. Falling back to Mock LLM.")
            llm = MockHydraulicLLM()
        else:
            llm = GeminiHydraulicLLM()


        rag = RAGEngine(llm_inference=llm)
        response = rag.predict(args.symptom)
        
        print("\n=== DIAGNOSTIC REPORT ===")
        print(response)
        print("=========================")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Tip: Run 'python main.py --ingest' first (ensure you have PDFs in data/pdfs)")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
