import os
import matplotlib.pyplot as plt  # Make sure to import this correctly
import pandas as pd
import seaborn as sns

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
                annot_kws={"size": 8}  # Smaller font for annotations
            )

            # Rotate x and y axis labels
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.yticks(rotation=0, fontsize=10)

            plt.title(f"Sensitivity Analysis Heatmap: {filename}", fontsize=14)
            
            # Save heatmap as image
            image_filename = os.path.splitext(filename)[0] + '.png'
            image_path = os.path.join('heatmap_images', image_filename)
            plt.tight_layout()
            plt.savefig(image_path, dpi=300)
            plt.close()

generate_images()
