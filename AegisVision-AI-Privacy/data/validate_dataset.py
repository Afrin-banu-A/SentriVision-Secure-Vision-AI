import pandas as pd
import sys

def validate():
    try:
        df = pd.read_csv("data/sensitive_text_dataset.csv")
    except FileNotFoundError:
        print("Dataset not found!")
        sys.exit(1)
        
    total_samples = len(df)
    
    # Check uniqueness
    unique_texts = df['text'].nunique()
    duplicate_count = total_samples - unique_texts
    
    # Check conflicting labels (same text, different label)
    label_counts = df.groupby('text')['label'].nunique()
    conflicting_labels = (label_counts > 1).sum()
    
    normal_count = len(df[df['label'] == 'NORMAL'])
    sensitive_count = len(df[df['label'] == 'SENSITIVE'])
    
    print(f"Total samples: {total_samples}")
    print(f"Unique samples: {unique_texts}")
    print(f"Duplicate count: {duplicate_count}")
    print(f"Conflicting label count: {conflicting_labels}")
    print(f"NORMAL count: {normal_count}")
    print(f"SENSITIVE count: {sensitive_count}")
    
    if duplicate_count > 0 or conflicting_labels > 0:
        print("Dataset validation FAILED.")
        sys.exit(1)
    else:
        print("Dataset validation PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    validate()
