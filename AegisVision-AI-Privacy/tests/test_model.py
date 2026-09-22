import os
import joblib
from backend.app.model_service import ModelService

def test_model_files_exist():
    assert os.path.exists("models/text_classifier.pkl")
    assert os.path.exists("models/tfidf_vectorizer.pkl")

def test_model_service_loading():
    service = ModelService()
    assert service.vectorizer is not None
    assert service.classifier is not None

def test_model_classification_normal():
    service = ModelService()
    prediction = service.predict("Machine learning is useful for data analysis.")
    assert prediction == "NORMAL"

def test_model_classification_sensitive():
    service = ModelService()
    prediction = service.predict("My email is demo@example.com")
    assert prediction == "SENSITIVE"
