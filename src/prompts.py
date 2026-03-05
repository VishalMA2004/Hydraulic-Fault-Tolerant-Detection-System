from langchain_core.prompts import PromptTemplate

# System Prompt: Defines the persona and strict safety rules
SYSTEM_PROMPT_TEMPLATE = """You are an expert Hydraulic Fault Diagnosis System. 
Your goal is to analyze the user's reported symptoms and provide a technical diagnosis using ONLY the context provided below.

STRICT RULES:
1. Use ONLY the provided context to answer. Do not use external knowledge.
2. If the answer is not in the context, say "I cannot identify the fault based on the available manuals."
3. Cite the source manual and section for your findings.
4. Provide a step-by-step mitigation or troubleshooting plan.
5. Maintain a professional, safety-first tone.

CONTEXT:
{context}
"""

# User Prompt: The specific query from the user
USER_PROMPT_TEMPLATE = """
SYMPTOM: {question}

Please analyze this symptom and provide a diagnosis and mitigation plan.
"""

def get_rag_prompt_template():
    """Combines system and user prompts."""
    full_template = SYSTEM_PROMPT_TEMPLATE + USER_PROMPT_TEMPLATE
    return PromptTemplate(
        template=full_template,
        input_variables=["context", "question"]
    )
