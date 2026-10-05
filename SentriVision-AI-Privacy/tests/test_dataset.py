import pandas as pd
import os

def test_dataset_exists():
    assert os.path.exists("data/sensitive_text_dataset.csv")

def test_dataset_uniqueness():
    df = pd.read_csv("data/sensitive_text_dataset.csv")
    total_samples = len(df)
    unique_texts = df['text'].nunique()
    
    assert total_samples > 500, "Dataset should have >500 samples"
    assert total_samples == unique_texts, "Dataset contains duplicates"

def test_dataset_no_conflicting_labels():
    df = pd.read_csv("data/sensitive_text_dataset.csv")
    label_counts = df.groupby('text')['label'].nunique()
    conflicting_labels = (label_counts > 1).sum()
    
    assert conflicting_labels == 0, "Dataset contains conflicting labels"
