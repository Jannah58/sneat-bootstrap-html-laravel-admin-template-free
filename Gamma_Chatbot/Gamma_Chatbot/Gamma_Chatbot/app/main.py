from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

OLLAMA_HOST = "http://ollama:11434"

class PromptRequest(BaseModel):
    prompt: str

class ChatRequest(BaseModel):
    message: str
    use_langchain: bool = True

@app.get("/", response_class=HTMLResponse)
def root():
    """Serve the main HTML page"""
    try:
        with open("static/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Frontend not found. Please check static/index.html</h1>")

@app.get("/status")
def check_model_status():
    """Check if Ollama model is ready"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            gemma_model = next((m for m in models if "gemma" in m["name"]), None)
            if gemma_model:
                return {"status": "ready", "model": gemma_model["name"]}
            else:
                return {"status": "no_model", "message": "No Gemma model found"}
        else:
            return {"status": "error", "message": "Ollama service not responding"}
    except requests.exceptions.RequestException as e:
        return {"status": "loading", "message": "Connecting to Ollama service..."}

@app.post("/generate")
def generate(request: PromptRequest):
    """Generate response from Ollama model"""
    try:
        # First check if model is available
        status_response = check_model_status()
        if status_response["status"] != "ready":
            raise HTTPException(status_code=503, detail="Model not ready")
        
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate", 
            json={
                "model": "gemma2:2b",
                "prompt": request.prompt,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from Ollama service")
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@app.post("/chat")
def chat_with_langchain(request: ChatRequest):
    """Generate response using LangChain with Gemma 2B model"""
    try:
        # First check if model is available
        status_response = check_model_status()
        if status_response["status"] != "ready":
            raise HTTPException(status_code=503, detail="Model not ready")
        
        if request.use_langchain:
            # Initialize LangChain Ollama
            llm = OllamaLLM(
                model="gemma2:2b",
                base_url="http://ollama:11434"
            )
            
            # Create a prompt template for better formatting
            prompt_template = PromptTemplate(
                input_variables=["question"],
                template="""You are a helpful AI assistant powered by Gemma 2B. Please provide a clear and concise response to the following question:

Question: {question}

Answer:"""
            )
            
            # Format the prompt
            formatted_prompt = prompt_template.format(question=request.message)
            
            # Generate response using LangChain
            response = llm(formatted_prompt)
            
            return {
                "response": response.strip(),
                "model": "gemma2:2b",
                "method": "langchain"
            }
        else:
            # Fallback to direct API call
            response = requests.post(
                f"{OLLAMA_HOST}/api/generate", 
                json={
                    "model": "gemma2:2b",
                    "prompt": request.message,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "response": result.get("response", ""),
                    "model": "gemma2:2b",
                    "method": "direct"
                }
            else:
                raise HTTPException(status_code=response.status_code, detail="Error from Ollama service")
                
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service error: {str(e)}")
