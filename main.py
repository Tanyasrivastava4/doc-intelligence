from fastapi import FastAPI, Request
from google.cloud import storage, documentai
from rag_engine import store_document, search_documents
from gemini_client import answer_question
from router_agent import router_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
import base64, json, asyncio

app = FastAPI()

PROJECT_ID = "doc-intelligence-495409"
LOCATION = "us"
PROCESSOR_ID = "9e1cad2bfbaf89d5"

session_service = InMemorySessionService()
runner = Runner(
    agent=router_agent,
    app_name="doc-intelligence",
    session_service=session_service
)

def extract_text(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    content = bucket.blob(file_name).download_as_bytes()
    client = documentai.DocumentProcessorServiceClient()
    name = f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"
    result = client.process_document(request=documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=content, mime_type="application/pdf")
    ))
    return result.document.text

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/process")
async def process_file(request: Request):
    body = await request.json()
    message = body.get("message", {})
    data = base64.b64decode(message.get("data", "")).decode("utf-8")
    event = json.loads(data)
    filename = event.get("name", "unknown")
    bucket_name = event.get("bucket", "")
    print(f"New file uploaded: {filename}")
    try:
        extracted_text = extract_text(bucket_name, filename)
        print(f"Extracted text preview: {extracted_text[:300]}")
        store_document(filename, extracted_text)
    except Exception as e:
        print(f"Error processing {filename}: {e}")
    return {"status": "received", "file": filename}

@app.get("/search")
def search(q: str):
    return {"results": search_documents(q)}

@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    question = body.get("question", "")
    chunks = search_documents(question, top_k=3)
    answer = answer_question(question, chunks)
    return {"question": question, "answer": answer}

@app.post("/agent")
async def agent_endpoint(request: Request):
    body = await request.json()
    user_message = body.get("message", "")
    session = await session_service.create_session(
        app_name="doc-intelligence",
        user_id="user1"
    )
    content = Content(parts=[Part(text=user_message)])
    response_text = ""
    async for event in runner.run_async(
        user_id="user1",
        session_id=session.id,
        new_message=content
    ):
        if event.is_final_response():
            response_text = event.response.text
    return {"response": response_text}