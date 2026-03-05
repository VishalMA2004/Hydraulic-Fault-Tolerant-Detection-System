# Intelligent Hydraulic Fault Prediction and Mitigation Using Fine-Tuned LLM with RAG

## 1. Abstract
This project presents a novel approach to predicting and mitigating hydraulic system faults by integrating Retrieval-Augmented Generation (RAG) with a domain-specific fine-tuned Large Language Model (LLM). Unlike generic AI models, this system relies exclusively on technical maintenance manuals and hydraulic engineering books to ensure high-fidelity, hallucination-free diagnostics. The system processes user-reported symptoms, retrieves relevant technical specifications and troubleshooting procedures from a vectorized knowledge base, and synthesizes accurate, actionable mitigation strategies using an LLM fine-tuned on instruction-response pairs derived from the same technical corpus. This dual approach combines the precision of retrieval with the reasoning capabilities of a fine-tuned model.

## 2. Industrial Use Cases
1.  **Automated Field Support**: Assists on-site technicians by providing instant diagnostic steps based on observed symptoms, reducing downtime.
2.  **Predictive Maintenance**: Analyzes reported symptom logs to identify recurring issues and suggest preventative replacements before catastrophic failure.
3.  **Training Assistant**: Serves as an interactive tutor for junior hydraulic engineers, explaining failure modes using verified technical data.
4.  **Offshore/Remote Operations**: Deployed in offline environments (oil rigs, ships) where expert human consultation is not immediately available.

---

## 3. System Architecture

The system operates on a hybrid pipeline combining vector retrieval and generative AI.

### High-Level Block Diagram

```ascii
                                   +---------------------+
                                   |  Technical Manuals  |
                                   | (PDFs/Hydraulic Books)|
                                   +----------+----------+
                                              |
                                     [Data Ingestion]
                                              |
       +--------------------------------------+--------------------------------------+
       |                                                                             |
[Chunking & Cleaning]                                                       [QA Pair Generation]
       |                                                                             |
 [Embedding Model]                                                           [Fine-Tuning Dataset]
       |                                                                             |
  +----v-----+                                                                  +----v-----+
  | Vector DB|                                                                  | Base LLM |
  | (FAISS)  |                                                                  +----+-----+
  +----+-----+                                                                       |
       |                                                                        [LoRA / QLoRA]
       |                                                                             |
       |             +---------------------------------------------------------------+
       |             |
       |      +------+------+
       +----->| RAG Engine  |<-----------------------+
              +------+------+                        |
                     |                        +------+------+
                     v                        | User Symptom|
              +--------------+                +-------------+
              | Final Prompt |
              +------+-------+
                     |
              +------v-------+
              | Fine-Tuned   |
              |     LLM      |
              +------+-------+
                     |
              +------v-------+
              |  Diagnostic  |
              | Output & Fix |
              +--------------+
```

### Why RAG + Fine-Tuning?
-   **RAG (Retrieval-Augmented Generation)**: Ensures the model has access to the exact, up-to-date specifications (e.g., "valve pressure set to 250 bar"). It prevents the model from inventing non-existent parts or procedures.
-   **Fine-Tuning**: Adapts the *style* and *reasoning process* of the LLM to think like a hydraulic expert. It teaches the model how to interpret the retrieved chunks and formulate a professional diagnostic report, rather than just summarizing text.

---

## 4. Data Sources

### Source Material
-   **Primary**: OEM Hydraulic Troubleshooting Manuals (e.g., Bosch Rexroth, Eaton, Parker).
-   **Secondary**: Handbooks on Fluid Power Engineering.

### Justification
Troubleshooting manuals are structured (Symptom -> Cause -> Remedy), making them ideal for both retrieval (finding the specific symptom) and generating training data (learning the logic of diagnosis).

### Data Format & Strategy
-   **Format**: PDF and DOCX.
-   **Chunking Strategy**:
    -   **Size**: 512 - 1024 tokens. Large enough to contain a full "Symptom-Cause-Solution" block but small enough to be specific.
    -   **Overlap**: 10-15% to preserve context between pages or section breaks.
    -   **Metadata**: Each chunk is tagged with `Book_Title`, `Chapter`, and `Page_Number` for citation.

---

## 5. Fine-Tuning Strategy

We do **not** fine-tune on raw book text (which creates "parrot" models). We fine-tune on **instructions** derived from the text.

### Methodology
1.  **Data Extraction**: Use an LLM to parse the manuals and generate Q&A pairs.
2.  **Dataset Usage**: 
    -   **Input**: "The system pressure fluctuates rapidly during idle."
    -   **Target**: "Check the accumulator pre-charge pressure. If low, recharge to X specification. Inspect the pressure relief valve for instability."
3.  **Technique**: **QLoRA (Quantized Low-Rank Adaptation)**. This allows fine-tuning 7B+ parameter models on consumer hardware by freezing the base model and training only a small set of adapter weights.

### What is Learned?
-   **Domain Terminology**: Understanding "cavitation", "learned load sensing", "swashplate angle".
-   **Diagnostic Logic**: The step-by-step deductive process (Check A -> If OK, Check B).
-   **Output Format**: Structuring answers as professional technical reports.

### JSONL Training Data Example
```json
{"messages": [
    {"role": "user", "content": "The hydraulic cylinder extends but does not retract. What is the potential cause?"},
    {"role": "assistant", "content": "Based on standard hydraulic schematics, this issue often indicates a failure in the directional control valve (DCV) solenoid or a blocked return line. Check if the 'B' side solenoid is energizing. Also, inspect the pilot check valve for jamming."}
]}
```

---

## 6. Model Selection

### Recommended Stack
1.  **LLM**: **Llama-3-8B-Instruct** or **Mistral-7B-Instruct-v0.2**.
    -   *Reason*: State-of-the-art reasoning capabilities in small sizes, permissible licenses, and excellent support for LoRA.
2.  **Embedding Model**: **BAAI/bge-large-en-v1.5**.
    -   *Reason*: Top performer on MTEB (Massive Text Embedding Benchmark) for retrieval tasks.
3.  **Vector Database**: **FAISS (Facebook AI Similarity Search)**.
    -   *Reason*: Lightweight, extremely fast for local deployment, and easy to integrate with Python.
4.  **Fine-Tuning Framework**: **Unsloth** or **Axolotl**.
    -   *Reason*: Unsloth provides 2-5x faster training and 50% less memory usage for QLoRA.

---

## 7. Evaluation Metrics

1.  **Groundedness Score (RAGAS)**: Measures how much of the answer is directly supported by the retrieved chunks. Target: > 0.9.
2.  **Answer Relevance**: Does the answer actually address the specific hydraulic symptom?
3.  **Hallucination Rate**: Percentage of generated facts (e.g., pressure values) that do not exist in the source text. Target: 0%.
4.  **Expert Validation**: A simplified "human-in-the-loop" check where a domain expert rates 50 random samples on a 1-5 Likert scale for technical accuracy.

---

## 8. Deployment Strategy

### Folder Structure
```
/project_root
├── /data
│   ├── /pdfs          # Raw manuals
│   └── /vector_store  # FAISS index
├── /src
│   ├── data_ingestion.py
│   ├── rag_engine.py
│   ├── fine_tune.py
│   └── main.py
├── /docs
│   └── Project_Report.md
└── requirements.txt
```

### Deployment Options
1.  **Online / Cloud**: Containerize with Docker and deploy the API (FastAPI) on AWS/Azure GPU instances. Front-end via Streamlit.
2.  **Offline / Edge**: Convert the fine-tuned model to GGUF format (llama.cpp) to run on CPU-only laptops or ruggedized industrial tablets usable in the field.

---
