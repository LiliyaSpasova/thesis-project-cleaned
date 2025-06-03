
import pandas as pd
from scipy.stats import pearsonr
import re

def extract_coeff(expr, term):
    expr = expr.replace(' ', '')
    pattern = rf'([+-]?\d*\.?\d+)\s*·?{term}'
    match = re.search(pattern, expr)
    return float(match.group(1)) if match else 0.0

def extract_c5(expr):
    expr = expr.replace(' ', '')
    # Split numerator and denominator
    if '/' not in expr:
        return 0.0
    _, denom = expr.split('/')
    denom = denom.strip('()')
    # Extract the coefficient before `xy` in the denominator
    match = re.search(r'([+-]?\d*\.?\d+)\s*·?xy', denom)
    return float(match.group(1)) if match else 0.0

# === Specify your CSV file here ===
file_path = "split_outputs_high_with_evidence_grouped_by_evidence_csv\\evidence__C__True.csv"

# Load data
df = pd.read_csv(file_path)

print(f"Total number of rows: {len(df)}")

# Extract coefficients
df['c1_coeff'] = df['Two-way Sens Function'].apply(lambda x: extract_coeff(x, 'xy'))
df['c5_coeff'] = df['Two-way Sens Function'].apply(extract_c5)

# Correlation analyses
r_c1, p_c1 = pearsonr(df['Sensitivity value'], df['c1_coeff'])
r_c5, p_c5 = pearsonr(df['Sensitivity value'], df['c5_coeff'])

print(f"\nCorrelation between Sensitivity value and interaction term (c1): r = {r_c1:.4f}, p = {p_c1:.4f}")
print(f"Correlation between Sensitivity value and denominator interaction term (c5): r = {r_c5:.4f}, p = {p_c5:.4f}")

# Show unique values
print("\nUnique values in 'Sensitivity value':", df['Sensitivity value'].unique())
print("Unique values in 'c1_coeff':", df['c1_coeff'].unique())
print("Unique values in 'c5_coeff':", df['c5_coeff'].unique())
