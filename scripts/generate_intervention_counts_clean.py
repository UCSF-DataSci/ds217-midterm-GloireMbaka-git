import sys
from pathlib import Path
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

from q3_data_utils import load_data, clean_data

# Load and clean
csv_path = repo_root / 'data' / 'clinical_trial_raw.csv'
df = load_data(str(csv_path))
df = clean_data(df)

# Count intervention groups
interv_counts = df['intervention_group'].value_counts().reset_index()
interv_counts.columns = ['intervention_group', 'count']

# Save
out = repo_root / 'output' / 'q4_intervention_counts.csv'
out.parent.mkdir(parents=True, exist_ok=True)
interv_counts.to_csv(out, index=False)

# Print top lines
print(interv_counts.head(30).to_string(index=False))
