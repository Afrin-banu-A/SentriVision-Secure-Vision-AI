import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os
from preprocess import preprocess_text

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error
import numpy as np

def train_model():
    print("Loading dataset...")
    df = pd.read_csv("data/sensitive_text_dataset.csv")
    
    print(f"Total samples: {len(df)}")
    
    # Preprocess texts
    df['processed_text'] = df['text'].apply(preprocess_text)
    
    # Split data (80/20)
    X = df['processed_text']
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    
    # IMPORTANT: Fit ONLY on training data
    print("Fitting TF-IDF on training data...")
    X_train_tfidf = vectorizer.fit_transform(X_train)
    
    # Transform test data
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Train Logistic Regression
    print("Training Logistic Regression model...")
    clf = LogisticRegression(random_state=42, max_iter=1000)
    clf.fit(X_train_tfidf, y_train)
    
    # Evaluate model
    print("Evaluating model...")
    y_pred = clf.predict(X_test_tfidf)
    # The classes in clf are clf.classes_. To find the index for 'SENSITIVE':
    pos_idx = list(clf.classes_).index('SENSITIVE')
    y_prob = clf.predict_proba(X_test_tfidf)[:, pos_idx]
    
    y_test_num = (y_test == 'SENSITIVE').astype(int)
    y_pred_num = (y_pred == 'SENSITIVE').astype(int)
    
    acc = accuracy_score(y_test_num, y_pred_num)
    prec = precision_score(y_test_num, y_pred_num)
    rec = recall_score(y_test_num, y_pred_num)
    f1 = f1_score(y_test_num, y_pred_num)
    cm = confusion_matrix(y_test_num, y_pred_num)
    
    # RMSE is included as an additional error metric for evaluation.
    # Classification metrics remain the primary evaluation metrics.
    rmse_class = np.sqrt(mean_squared_error(y_test_num, y_pred_num))
    rmse_prob = np.sqrt(mean_squared_error(y_test_num, y_prob))
    
    print("\n--- Model Evaluation ---")
    print(f"Accuracy: {acc}")
    print(f"Precision: {prec}")
    print(f"Recall: {rec}")
    print(f"F1-score: {f1}")
    print(f"Classification RMSE: {rmse_class}")
    print(f"Probability RMSE: {rmse_prob}")
    print("Confusion Matrix:")
    print(cm)
    print("------------------------\n")
    
    # Ensure models directory exists
    os.makedirs('models', exist_ok=True)
    
    # Save models
    print("Saving models...")
    joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')
    joblib.dump(clf, 'models/text_classifier.pkl')
    
    print("Model training complete. Models saved to models/ directory.")

if __name__ == "__main__":
    train_model()
