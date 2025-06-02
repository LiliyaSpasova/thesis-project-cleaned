import os
import matplotlib.pyplot as plt  # Make sure to import this correctly
import pandas as pd
import seaborn as sns
import numpy as np 
def generate_images():
    for filename in os.listdir('heatmaps'):
        if filename.endswith('.csv'):
            filepath = os.path.join('heatmaps', filename)
            
            # Load sensitivity matrix
            sensitivity_matrix = pd.read_csv(filepath, index_col=0)

            # Plot heatmap with improved readability
            plt.figure(figsize=(30, 24))  # Larger figure
            ax = sns.heatmap(
                sensitivity_matrix, 
                cmap="coolwarm", 
                annot=True, 
                fmt=".2f", 
                linewidths=0.8, 
                annot_kws={"size": 12}  # Smaller font for annotations
            )

            # Rotate x and y axis labels
            plt.xticks(rotation=45, ha='right', fontsize=16)
            plt.yticks(rotation=0, fontsize=28)

            plt.title(f"Sensitivity Analysis Heatmap: {filename}", fontsize=14)
            
            # Save heatmap as image
            image_filename = os.path.splitext(filename)[0] + '.png'
            image_path = os.path.join('heatmap_images', image_filename)
            plt.tight_layout()
            plt.savefig(image_path, dpi=300)
            plt.close()


def generate_tank_heatmaps():
    for filename in os.listdir('heatmaps'):
        if filename.startswith('Tank') and filename.endswith('.csv'):
            filepath = os.path.join('heatmaps', filename)

            # Load the CSV
            df = pd.read_csv(filepath, index_col=0)

            # Drop all-zero columns and rows
            df_cleaned = df.loc[(df != 0).any(axis=1), (df != 0).any(axis=0)]

            if df_cleaned.empty:
                print(f"Skipped {filename}: only zeros after cleaning.")
                continue

            # Mask remaining zero values for cleaner visualization
            df_masked = df_cleaned.replace(0, np.nan)
            mask = df_masked.isnull()

            # Plot
            plt.figure(figsize=(30, 24))
            sns.heatmap(
                df_masked,
                cmap="coolwarm",
                annot=True,
                fmt=".2f",
                linewidths=0.8,
                annot_kws={"size": 8},
                mask=mask,
                cbar_kws={"label": "Sensitivity"}
            )

            # Axes styling
            plt.xticks(rotation=45, ha='right', fontsize=14)
            plt.yticks(rotation=0, fontsize=28)
            plt.title(f"Sensitivity Analysis Heatmap: {filename}", fontsize=20)

            # Save
            os.makedirs('heatmap_images', exist_ok=True)
            image_filename = os.path.splitext(filename)[0] + '.png'
            image_path = os.path.join('heatmap_images', image_filename)
            plt.tight_layout()
            plt.savefig(image_path, dpi=300)
            plt.close()

generate_images()
