import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def distribution_analysis(csv_path: str):
    # Read data
    df = pd.read_csv(csv_path)
    
    # Define columns to plot
    numeric_cols = ['age', 'annual_income', 'credit_score']
    funnel_cols = ['assigned', 'worked', 'contacted', 'appointment']
    
    # Total number of subplots
    total_plots = len(numeric_cols) + len(funnel_cols)
    
    # Calculate grid layout (for example, 2 rows)
    rows = 2
    cols = (total_plots + 1) // rows  # ensures enough columns
    
    # Create figure with subplots
    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(5 * cols, 5 * rows))
    axes = axes.flatten()  # flatten the array of Axes objects
    
    # Plot numeric columns
    for i, col in enumerate(numeric_cols):
        sns.histplot(data=df, x=col, kde=True, ax=axes[i])
        axes[i].set_title(f'{col} Distribution')
    
    # Plot funnel columns
    for j, col in enumerate(funnel_cols):
        idx = len(numeric_cols) + j  # position in subplots
        sns.countplot(data=df, x=col, ax=axes[idx])
        axes[idx].set_title(f'{col} Distribution')
        
    # Hide any leftover subplots if not used
    for k in range(total_plots, len(axes)):
        axes[k].set_visible(False)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    distribution_analysis("/Users/nikhilmaddikunta/Desktop/Nikhil/others/office/project/output/sample_data.csv")
```
