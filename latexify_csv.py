import pandas as pd

def latexify(expr):
    return f"$\\frac{{{expr.split('/')[0].strip()}}}{{{expr.split('/')[1].strip()}}}$" if '/' in expr else f"${expr.strip()}$"

df = pd.read_csv("split_outputs_high_no_evidence_csv\\PB__False__MC__False__PCT__False__B__False.csv")

with open("latex_table.tex", "w", encoding="utf-8") as f:
    f.write("\\begin{tabular}{|l|l|c|l|l|l|l|}\n\\hline\n")
    f.write("Param1 & Param2 & Sens. & Target  & 2-way Sens \\\\\n\\hline\n")
    for _, row in df.iterrows():
        line = " & ".join([
            f"${row['Param1']}$",
            f"${row['Param2']}$",
            str(row['Sensitivity value']),
            f"${row['Target']}$",
            latexify(row['Two-way Sens Function']),
        ])
        f.write(line + " \\\\\n\\hline\n")
    f.write("\\end{tabular}\n")
