from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

def process_document_tool(bucket_name: str, file_name: str) -> str:
    from main import extract_text
    from rag_engine import store_document
    text = extract_text(bucket_name, file_name)
    store_document(file_name, text)
    return f"Document {file_name} processed and stored successfully. Extracted {len(text)} characters."

ocr_agent = LlmAgent(
    name="ocr_agent",
    model="gemini-2.5-flash",
    instruction="You process uploaded PDF documents. Extract text and store it.",
    tools=[FunctionTool(process_document_tool)]
)