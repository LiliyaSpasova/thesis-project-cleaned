import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# Load from CSV
sensitivity_matrix = pd.read_csv("sensitivity_matrix.csv", index_col=0)

# Iterate through the matrix and print positive values with their labels
positive_values = []

for x_label in sensitivity_matrix.index:  # Row names
    for y_label in sensitivity_matrix.columns:  # Column names
        value = sensitivity_matrix.at[x_label, y_label]
        if value > 0:  # Filter positive values
            positive_values.append((x_label, y_label, value))

# Display results
for x, y, val in positive_values:
    print(f"P({x} | {y}) = {val:.4f}")


# Adjust figure size
plt.figure(figsize=(26, 8))

# Plot heatmap with larger figure and rotated labels
sns.heatmap(
    sensitivity_matrix,
    cmap="coolwarm",
    annot=True,
    fmt=".2f",
    linewidths=0.5,
    annot_kws={"size": 7}  # Increase annotation font size
)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Increase bottom margin and apply tight layout
plt.subplots_adjust(bottom=0.4)
plt.tight_layout()

# Show plot
plt.show()
