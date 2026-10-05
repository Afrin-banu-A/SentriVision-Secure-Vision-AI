from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.app.schemas import SanitizeRequest, SanitizeResponse, AIProcessRequest, AIProcessResponse
from backend.app.sanitizer import AegisSanitizer
from backend.app.model_service import ModelService
import re

app = FastAPI(title="SentriVision Privacy Gateway")

# Allow CORS for the local extension and demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In a real scenario, this would be restricted to the extension ID and 127.0.0.1
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
sanitizer = AegisSanitizer()
model_service = ModelService()

@app.get("/")
def read_root():
    return {
        "status": "running",
        "project": "SentriVision",
        "mode": "local_privacy_gateway"
    }

@app.post("/sanitize", response_model=SanitizeResponse)
def sanitize_text(request: SanitizeRequest):
    if not request.text:
        return SanitizeResponse(
            detected=False,
            original_length=0,
            sanitized_length=0,
            sanitized_text="",
            entities=[],
            protected_count=0,
            classification="NORMAL"
        )
        
    # 1. Run ML classification
    ml_classification = model_service.predict(request.text)
    
    # 2. Run deterministic entity detection and sanitization
    sanitization_result = sanitizer.sanitize(request.text)
    
    # 3. Strictly enforce classification rule based on validated entities
    if sanitization_result["protected_count"] >= 1 and len(sanitization_result["entities"]) >= 1:
        final_classification = "SENSITIVE"
        final_detected = True
    else:
        final_classification = "NORMAL"
        final_detected = False
    
    return SanitizeResponse(
        detected=final_detected,
        original_length=sanitization_result["original_length"],
        sanitized_length=sanitization_result["sanitized_length"],
        sanitized_text=sanitization_result["sanitized_text"],
        entities=sanitization_result["entities"],
        protected_count=sanitization_result["protected_count"],
        classification=final_classification
    )

@app.post("/ai/process", response_model=AIProcessResponse)
def ai_process(request: AIProcessRequest):
    """
    Simulates the external AI backend endpoint.
    It should ONLY receive sanitized text.
    We implement a safety check to reject obvious raw PII if accidentally sent.
    """
    raw_text = request.text
    
    # Use the existing sanitizer to detect if any supported raw PII is still present
    sanitization_result = sanitizer.sanitize(raw_text)
    
    if sanitization_result["detected"]:
        return AIProcessResponse(
            status="REJECTED",
            reason="Potential raw sensitive information detected",
            privacy_safe=False,
            received_by_ai=raw_text
        )

    # If it passed safety checks, it's processed
    return AIProcessResponse(
        status="ACCEPTED",
        message="AI-safe content received",
        privacy_safe=True,
        received_by_ai=raw_text
    )

@app.post("/detect-sensitive-text", response_model=SanitizeResponse)
def detect_sensitive_text(request: SanitizeRequest):
    """
    Endpoint that clearly separates Classification from Entity detection.
    """
    return sanitize_text(request)


