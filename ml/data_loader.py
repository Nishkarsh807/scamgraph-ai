"""
ScamGraph AI - Data Loader
Loads and validates train, validation, and test splits.
"""

import os
import pandas as pd
from typing import Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_splits() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load train, validation, and test datasets.
    Returns: (train_df, val_df, test_df)
    """
    train_path = os.path.join(DATA_DIR, "train.csv")
    val_path = os.path.join(DATA_DIR, "validation.csv")
    test_path = os.path.join(DATA_DIR, "test.csv")

    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Missing train data at {train_path}. Run dataset_generator.py first.")

    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)

    return train_df, val_df, test_df

if __name__ == "__main__":
    train, val, test = load_splits()
    print(f"Loaded datasets successfully: Train={len(train)}, Val={len(val)}, Test={len(test)}")
