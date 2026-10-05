import joblib
import os
import sys

class ModelService:
    def __init__(self):
        self.vectorizer = None
        self.classifier = None
        self._load_models()

    def _load_models(self):
        try:
            # We assume we are running from the project root
            self.vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
            self.classifier = joblib.load('models/text_classifier.pkl')
            print("ML models loaded successfully.")
        except FileNotFoundError:
            print("Warning: ML models not found. Please run ML training first.")
            self.vectorizer = None
            self.classifier = None

    def predict(self, text: str) -> str:
        if not self.vectorizer or not self.classifier:
            return "UNKNOWN"
            
        # Basic preprocessing (similar to what was used in training)
        processed_text = text.lower().strip()
        
        # Transform and predict
        X_tfidf = self.vectorizer.transform([processed_text])
        prediction = self.classifier.predict(X_tfidf)
        
        return prediction[0]
