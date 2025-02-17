import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def distribution_analysis(csv_path: str, output_dir: str):
    # Read data
    df = pd.read_csv(csv_path)
    
    # Define columns to plot
    numeric_cols = ['age', 'annual_income', 'credit_score']
    funnel_cols = ['assigned', 'worked', 'contacted', 'appointment']
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Plot numeric columns
    for col in numeric_cols:
        plt.figure(figsize=(8, 6))
        sns.histplot(data=df, x=col, kde=True)
        plt.title(f'{col} Distribution')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'{col}_distribution.png'))
        plt.close()
        
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=df, x=col)
        plt.title(f'{col} Box Plot')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'{col}_boxplot.png'))
        plt.close()
    
    # Plot funnel columns
    for col in funnel_cols:
        plt.figure(figsize=(8, 6))
        sns.countplot(data=df, x=col)
        plt.title(f'{col} Distribution')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'{col}_distribution.png'))
        plt.close()
