from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

def answer_from_documents_tool(question: str) -> str:
    from rag_engine import search_documents
    from gemini_client import answer_question
    chunks = search_documents(question)
    return answer_question(question, chunks)

rag_agent = LlmAgent(
    name="rag_agent",
    model="gemini-2.5-flash",
    instruction="You answer questions about uploaded documents using the search tool.",
    tools=[FunctionTool(answer_from_documents_tool)]
)