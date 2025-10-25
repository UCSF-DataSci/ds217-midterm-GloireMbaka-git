import sys
from pathlib import Path
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

from q3_data_utils import load_data, clean_data

raw_path = repo_root / 'data' / 'clinical_trial_raw.csv'
df_raw = load_data(str(raw_path))

print('--- Site counts BEFORE clean ---')
print(df_raw['site'].value_counts().head(20))
print('\n--- Intervention counts BEFORE clean ---')
print(df_raw['intervention_group'].value_counts().head(20))

# Apply cleaning
from q3_data_utils import clean_data

df_clean = clean_data(df_raw.copy())
print('\n--- Site counts AFTER clean ---')
print(df_clean['site'].value_counts().head(20))
print('\n--- Intervention counts AFTER clean ---')
print(df_clean['intervention_group'].value_counts().head(20))
