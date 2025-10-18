from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl, EmailStr
from uuid import uuid4
import httpx
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware 

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Agent Backend")

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# --- CORS CONFIGURATION ---
# The origins array must contain the exact address of your frontend.
# http://localhost:8080 is correctly added to fix the initial CORS error.
origins = [
    "http://localhost:8080",      # Your frontend development server
    "http://127.0.0.1:8080",
    "http://localhost:3000",      # Common React/Next.js default
    # If running on Lovable, add your specific preview domain here
    # e.g., "https://my-lovable-app.lovable.dev",
]

# Add the CORSMiddleware to your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,      # Allow cookies/auth headers (if you plan to use them)
    allow_methods=["*"],         # Allow all standard HTTP methods (GET, POST, etc.)
    allow_headers=["*"],         # Allow all request headers
)
# ----------------------------

# Input schema
class ArticleRequest(BaseModel):
    email: EmailStr
    article_url: HttpUrl

# --- HEALTH CHECK ENDPOINT (Added for completeness) ---
@app.get("/health")
def health_check():
    """Simple endpoint to confirm the API is running and configured."""
    return {
        "status": "ok", 
        "service": "AI Agent Backend",
        "webhook_configured": N8N_WEBHOOK_URL is not None and N8N_WEBHOOK_URL != ""
    }


@app.post("/process-article")
async def process_article(request: ArticleRequest):
    """
    Receives email + article_url from frontend,
    generates session_id, and sends to n8n webhook.
    """
    
    if not N8N_WEBHOOK_URL:
        # Configuration check
        raise HTTPException(
            status_code=503,
            detail="Backend not fully configured. N8N_WEBHOOK_URL environment variable is missing."
        )

    session_id = str(uuid4())

    payload = {
        "email": request.email,
        "article_url": str(request.article_url),
        "session_id": session_id
    }

    try:
        # Use httpx.AsyncClient for making asynchronous HTTP requests
        async with httpx.AsyncClient(timeout=30) as client:
            
            response = await client.post(N8N_WEBHOOK_URL, json=payload) 
            response.raise_for_status() # Raises HTTPStatusError if the response status is 4xx or 5xx

        # If the request was successful (2xx status code)
        return {
            "status": "success",
            "session_id": session_id,
            "message": "Data successfully sent to n8n webhook"
        }

    except httpx.ConnectError:
        # Handle connection issues (e.g., n8n service is down or URL is unreachable)
        raise HTTPException(
            status_code=503,
            detail=f"Connection error: Could not reach the webhook URL at {N8N_WEBHOOK_URL}. Check if n8n is running."
        )
    except httpx.HTTPStatusError as e:
        # Handle error responses from the n8n webhook itself (4xx or 5xx from the webhook)
        print("❌ n8n Error Response:", e.response.text)
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Failed to send data to n8n: Webhook returned status code {e.response.status_code}. Detail: {e.response.text}"
        )
    except Exception as e:
        # Catch all other exceptions
        print(f"Httpx Exception: {e}") 
        raise HTTPException(
            status_code=500, 
            detail=f"An unexpected internal server error occurred: {str(e)}"
        )
