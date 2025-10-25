import sys
from pathlib import Path
# Add repository root to sys.path so imports work when running from scripts/
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

from q3_data_utils import load_data, clean_data
from IPython.display import display
import pandas as pd

# Load data
df = load_data(str(repo_root / 'data' / 'clinical_trial_raw.csv'))
print(f"Loaded {len(df)} patients with {len(df.columns)} variables")

print("Shape of the dataset:", df.shape)
print("Columns in the dataset:", df.columns.tolist())
print("Data types:\n", df.dtypes)

# First 10 rows
print("\nFirst 10 rows:")
print(df.head(10).to_string())

# Summary
print("\nSummary statistics (.describe):")
print(df.describe(include='all').to_string())
