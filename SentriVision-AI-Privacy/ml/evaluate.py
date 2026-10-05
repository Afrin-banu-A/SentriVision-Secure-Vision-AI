import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
from preprocess import preprocess_text
import sys

def evaluate_model():
    print("Loading dataset for evaluation...")
    try:
        df = pd.read_csv("data/sensitive_text_dataset.csv")
    except FileNotFoundError:
        print("Dataset not found! Please run generate_dataset.py first.")
        sys.exit(1)
        
    df['processed_text'] = df['text'].apply(preprocess_text)
    X = df['processed_text']
    y = df['label']
    
    # Split using same parameters as train to get the same test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    
    try:
        vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
        clf = joblib.load('models/text_classifier.pkl')
    except FileNotFoundError:
        print("Models not found! Please run train.py first.")
        sys.exit(1)
        
    print(f"Number of training samples: {len(X_train)}")
    print(f"Number of test samples: {len(X_test)}")
    
    unique_samples = df['text'].nunique()
    print(f"Number of unique samples: {unique_samples}")
    print(f"Duplicate count: {len(df) - unique_samples}")
    
    # Check overlap (should be 0)
    train_texts = set(X_train)
    test_texts = set(X_test)
    overlap = train_texts.intersection(test_texts)
    print(f"Train/test overlap: {len(overlap)}")
    
    print("\n--- ML Evaluation Metrics ---")
    
    X_test_tfidf = vectorizer.transform(X_test)
    y_pred = clf.predict(X_test_tfidf)
    
    acc = accuracy_score(y_test, y_pred)
    # Using pos_label='SENSITIVE' for precision/recall/f1 since it's a binary classification
    prec = precision_score(y_test, y_pred, pos_label='SENSITIVE')
    rec = recall_score(y_test, y_pred, pos_label='SENSITIVE')
    f1 = f1_score(y_test, y_pred, pos_label='SENSITIVE')
    cm = confusion_matrix(y_test, y_pred, labels=['NORMAL', 'SENSITIVE'])
    
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1-score: {f1:.4f}")
    
    print("\nConfusion Matrix [NORMAL, SENSITIVE]:")
    print(cm)

if __name__ == "__main__":
    evaluate_model()
