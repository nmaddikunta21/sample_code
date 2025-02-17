import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def normalized_bar_chart_by_reason_code(df: pd.DataFrame, output_path: str):
    
    # Create a new column for segmentation
    df['segment'] = 'assigned'
    df.loc[df['worked'] == 1, 'segment'] = 'worked'
    df.loc[df['contacted'] == 1, 'segment'] = 'contacted'
    df.loc[df['appointment'] == 1, 'segment'] = 'appointment'
    # Calculate the percentage for each segment within each reason code
    df['count'] = 1
    df_grouped = df.groupby(['reason_code', 'segment']).count().reset_index()
    df_total = df_grouped.groupby('reason_code')['count'].sum().reset_index()
    df_total = df_total.rename(columns={'count': 'total_count'})
    df_merged = pd.merge(df_grouped, df_total, on='reason_code')
    df_merged['percentage'] = df_merged['count'] / df_merged['total_count'] * 100
    df = pd.merge(df, df_merged[['reason_code', 'segment', 'percentage']], on=['reason_code', 'segment'], how='left')
    # Plot normalized bar chart for each reason code segmented by labels
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='reason_code', hue='segment', multiple='fill', shrink=0.8)
    plt.title('Normalized Bar Chart by Reason Code Segmented by Labels')
    plt.xlabel('Reason Code')
    plt.ylabel('Proportion')
    plt.legend(title='Segment')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    df = pd.read_csv("/Users/nikhilmaddikunta/Desktop/Nikhil/others/office/project/output/sample_data.csv")
    normalized_bar_chart_by_reason_code(
        df,
        "/Users/nikhilmaddikunta/Desktop/Nikhil/others/office/project/output/normalized_bar_chart_by_reason_code.png"
    )
