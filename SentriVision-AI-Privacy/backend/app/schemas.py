from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class SanitizeRequest(BaseModel):
    text: str = Field(..., description="The original webpage text to be sanitized")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Bank Account: 123456789012"
                }
            ]
        }
    }

class Entity(BaseModel):
    type: str
    placeholder: str

class SanitizeResponse(BaseModel):
    detected: bool
    original_length: int
    sanitized_length: int
    sanitized_text: str
    entities: List[Entity]
    protected_count: int
    classification: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "detected": True,
                    "original_length": 30,
                    "sanitized_length": 52,
                    "sanitized_text": "Bank Account: [BANK ACCOUNT REDACTED]",
                    "entities": [
                        {
                            "type": "BANK_ACCOUNT",
                            "placeholder": "[BANK ACCOUNT REDACTED]"
                        }
                    ],
                    "protected_count": 1,
                    "classification": "SENSITIVE"
                }
            ]
        }
    }

class AIProcessRequest(BaseModel):
    text: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Bank Account: [BANK ACCOUNT REDACTED]"
                }
            ]
        }
    }

class AIProcessResponse(BaseModel):
    status: str
    message: Optional[str] = None
    reason: Optional[str] = None
    privacy_safe: bool
    received_by_ai: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "ACCEPTED",
                    "message": "AI-safe content received",
                    "privacy_safe": True,
                    "received_by_ai": "Bank Account: [BANK ACCOUNT REDACTED]"
                }
            ]
        }
    }

