import re

def preprocess_text(text: str) -> str:
    """
    Basic text preprocessing:
    - Lowercase
    - Normalize whitespace
    - Keep basic punctuation for context
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
