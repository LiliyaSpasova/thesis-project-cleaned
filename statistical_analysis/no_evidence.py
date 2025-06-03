import os
import pandas as pd
from scipy.stats import pearsonr
import re

def extract_xy_coeff(expr):
    match = re.search(r'([+-]?\d*\.?\d+)\s*·?xy', expr.replace(' ', ''))
    if match:
        return float(match.group(1))
    else:
        return 0.0

folder_path = "split_outputs_high_no_evidence_csv"
all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

dfs = []
for file in all_files:
    df = pd.read_csv(file)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

print(f"Total number of rows in combined dataframe: {len(combined_df)}")

combined_df['xy_coeff'] = combined_df['Two-way Sens Function'].apply(extract_xy_coeff)

print(combined_df.head())

r, p = pearsonr(combined_df['Sensitivity value'], combined_df['xy_coeff'])
print(f"Correlation between Sensitivity value and coefficient of xy: r = {r:.4f}, p = {p:.4f}")
print("\nUnique values in 'Sensitivity value':", combined_df['Sensitivity value'].unique())
print("Unique values in 'xy_coeff':", combined_df['xy_coeff'].unique())