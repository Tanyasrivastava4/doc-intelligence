from google.adk.agents import LlmAgent
from ocr_agent import ocr_agent
from rag_agent import rag_agent

router_agent = LlmAgent(
    name="router",
    model="gemini-2.5-flash",
    instruction="""You are a coordinator.
    If the user wants to process or upload a document, delegate to ocr_agent.
    If the user asks a question about documents, delegate to rag_agent.""",
    sub_agents=[ocr_agent, rag_agent]
)