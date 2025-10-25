import sys
from pathlib import Path
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

from q3_data_utils import load_data, clean_data

# Load and clean
csv_path = repo_root / 'data' / 'clinical_trial_raw.csv'
df = load_data(str(csv_path))
df = clean_data(df)

# Count sites
site_counts = df['site'].value_counts().reset_index()
site_counts.columns = ['site', 'count']

# Save
out = repo_root / 'output' / 'q4_site_counts.csv'
out.parent.mkdir(parents=True, exist_ok=True)
site_counts.to_csv(out, index=False)

# Print top lines
print(site_counts.head(30).to_string(index=False))
