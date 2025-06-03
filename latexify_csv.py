import pandas as pd
import numpy as np
import os

def latexify(expr):
    return f"$\\frac{{{expr.split('/')[0].strip()}}}{{{expr.split('/')[1].strip()}}}$" if '/' in expr else f"${expr.strip()}$"

# === Load CSVs ===
folder_path = "split_outputs_high_with_evidence_grouped_by_evidence_csv"
all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

dfs = []
for file in all_files:
    df = pd.read_csv(file)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

# === Sample 20 rows with unique sensitivity values ===
sampled_df = (
    combined_df.groupby("Sensitivity value", group_keys=False)
    .apply(lambda g: g.sample(1, random_state=42))  # sample one per unique sensitivity value
    .sample(n=min(20, len(combined_df["Sensitivity value"].unique())), random_state=42)  # shuffle & limit
)

# === Write LaTeX table ===
with open("latex_table.tex", "w", encoding="utf-8") as f:
    f.write("\\begin{tabular}{|l|l|c|l|l|}\n\\hline\n")
    f.write("Param1 & Param2 & Sens. & Target & 2-way Sens \\\\\n\\hline\n")
    for _, row in sampled_df.iterrows():
        line = " & ".join([
            f"${row['Param1']}$",
            f"${row['Param2']}$",
            str(row['Sensitivity value']),
            f"${row['Target']}$",
            latexify(row['Two-way Sens Function']),
        ])
        f.write(line + " \\\\\n\\hline\n")
    f.write("\\end{tabular}\n")
