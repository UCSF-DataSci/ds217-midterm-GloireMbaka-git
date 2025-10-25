import sys
from pathlib import Path
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))
from q3_data_utils import load_data, clean_data

raw = load_data(str(repo_root / 'data' / 'clinical_trial_raw.csv'))
print('Raw sample enrollment_date (first 20):')
print(raw['enrollment_date'].head(20).to_string())

cleaned = clean_data(raw.copy())
print('\nCleaned sample enrollment_date (first 20):')
print(cleaned['enrollment_date'].head(20).to_string())

if 'enrollment_date_iso' in cleaned.columns:
    print('\nCleaned enrollment_date_iso (first 20):')
    print(cleaned['enrollment_date_iso'].head(20).to_string())

print('\nCleaned enrollment_date dtype:', cleaned['enrollment_date'].dtype)
print('Count parsed (notna):', cleaned['enrollment_date'].notna().sum())
print('Count unparsed (isna):', cleaned['enrollment_date'].isna().sum())

# show unique string patterns for raw values (sample)
print('\nUnique raw examples (up to 30):')
print(raw['enrollment_date'].dropna().astype(str).unique()[:30])
