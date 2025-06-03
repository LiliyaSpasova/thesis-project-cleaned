import os
import pandas as pd
from scipy.stats import pearsonr
import re

def extract_coeff(expr, term):
    expr = expr.replace(' ', '')
    pattern = rf'([+-]?\d*\.?\d+)\s*·?{term}'
    match = re.search(pattern, expr)
    if match:
        return float(match.group(1))
    else:
        return 0.0

def extract_c5(expr):
    expr = expr.replace(' ', '')
    if '/' not in expr:
        return 0.0
    try:
        denominator = expr.split('/')[-1]  # Get the denominator part
        pattern = r'([+-]?\d*\.?\d+)\s*·?xy'
        match = re.search(pattern, denominator)
        if match:
            return float(match.group(1))
        else:
            return 0.0
    except Exception:
        return 0.0


folder_path = "split_outputs_high_with_evidence_grouped_by_evidence_csv"
all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

dfs = []
for file in all_files:
    df = pd.read_csv(file)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

print(f"Total number of rows in combined dataframe: {len(combined_df)}")

combined_df['c1_coeff'] = combined_df['Two-way Sens Function'].apply(lambda x: extract_coeff(x, 'xy'))
combined_df['c5_coeff'] = combined_df['Two-way Sens Function'].apply(extract_c5)

print(combined_df.head())

# Correlation analyses
r_c1, p_c1 = pearsonr(combined_df['Sensitivity value'], combined_df['c1_coeff'])
r_c5, p_c5 = pearsonr(combined_df['Sensitivity value'], combined_df['c5_coeff'])

print(f"\nCorrelation between Sensitivity value and interaction term (c1): r = {r_c1:.4f}, p = {p_c1:.4f}")
print(f"Correlation between Sensitivity value and constant term (c5): r = {r_c5:.4f}, p = {p_c5:.4f}")

print("\nUnique values in 'Sensitivity value':", combined_df['Sensitivity value'].unique())
print("Unique values in 'c1_coeff':", combined_df['c1_coeff'].unique())
print("Unique values in 'c5_coeff':", combined_df['c5_coeff'].unique())