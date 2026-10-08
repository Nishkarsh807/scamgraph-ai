"""
ScamGraph AI - Exploratory Data Analysis & Feature Verification
This script conducts exploratory data analysis on the Indian fraud communications dataset.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "scam_dataset_raw.csv")

def run_eda():
    if not os.path.exists(DATA_PATH):
        print(f"Dataset not found at {DATA_PATH}. Run ml/dataset_generator.py first.")
        return

    df = pd.read_csv(DATA_PATH)
    print("=" * 60)
    print("SCAMGRAPH AI - DATASET EXPLORATION")
    print("=" * 60)
    print(f"Total Records: {len(df)}")
    print("\n--- Label Distribution ---")
    print(df["label"].value_counts(normalize=True).round(3) * 100)
    print("\n--- Scam Category Counts ---")
    print(df["scam_type"].value_counts())
    print("\n--- Language Representation ---")
    print(df["language"].value_counts())
    print("\n--- Average Character Length ---")
    df["char_len"] = df["text"].apply(len)
    print(df.groupby("label")["char_len"].mean().round(1))
    print("=" * 60)

if __name__ == "__main__":
    run_eda()
