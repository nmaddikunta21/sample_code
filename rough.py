import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(os.path.dirname(script_dir), 'output', 'sample_data.csv')
    return pd.read_csv(data_path)

def create_overall_funnel(df):
    """Create an overall funnel visualization showing conversion at each stage."""
    stages = ['Total', 'Assigned', 'Worked', 'Contacted', 'Appointment']
    values = [
        len(df),
        df['assigned'].sum(),
        df['worked'].sum(),
        df['contacted'].sum(),
        df['appointment'].sum()
    ]
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial"
    ))
    
    fig.update_layout(title='Overall Conversion Funnel',
                     width=800,
                     height=500)
    return fig

def create_segment_funnel(df):
    """Create funnel analysis by customer segment."""
    segments = df['customer_segment'].unique()
    fig = plt.figure(figsize=(12, 6))
    
    segment_metrics = []
    for segment in segments:
        segment_data = df[df['customer_segment'] == segment]
        total = len(segment_data)
        metrics = {
            'Segment': segment,
            'Assigned Rate': (segment_data['assigned'].sum() / total) * 100,
            'Worked Rate': (segment_data['worked'].sum() / total) * 100,
            'Contacted Rate': (segment_data['contacted'].sum() / total) * 100,
            'Appointment Rate': (segment_data['appointment'].sum() / total) * 100
        }
        segment_metrics.append(metrics)
    
    segment_df = pd.DataFrame(segment_metrics)
    segment_df_melted = pd.melt(segment_df, 
                               id_vars=['Segment'],
                               var_name='Stage',
                               value_name='Conversion Rate')
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=segment_df_melted, 
                x='Stage', 
                y='Conversion Rate', 
                hue='Segment')
    plt.xticks(rotation=45)
    plt.title('Conversion Rates by Customer Segment')
    plt.tight_layout()
    return plt.gcf()

def create_region_funnel(df):
    """Create funnel analysis by region."""
    regions = df['region'].unique()
    region_metrics = []
    
    for region in regions:
        region_data = df[df['region'] == region]
        total = len(region_data)
        metrics = {
            'Region': region,
            'Assigned Rate': (region_data['assigned'].sum() / total) * 100,
            'Worked Rate': (region_data['worked'].sum() / total) * 100,
            'Contacted Rate': (region_data['contacted'].sum() / total) * 100,
            'Appointment Rate': (region_data['appointment'].sum() / total) * 100
        }
        region_metrics.append(metrics)
    
    region_df = pd.DataFrame(region_metrics)
    region_df_melted = pd.melt(region_df,
                              id_vars=['Region'],
                              var_name='Stage',
                              value_name='Conversion Rate')
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=region_df_melted,
                x='Region',
                y='Conversion Rate',
                hue='Stage')
    plt.title('Conversion Rates by Region')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt.gcf()

def save_plots(figs, output_dir):
    """Save all generated plots."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save plotly figure
    figs['overall'].write_html(os.path.join(output_dir, 'overall_funnel.html'))
    
    # Save matplotlib figures
    figs['segment'].savefig(os.path.join(output_dir, 'segment_funnel.png'))
    figs['region'].savefig(os.path.join(output_dir, 'region_funnel.png'))

if __name__ == "__main__":
    # Load the data
    df = load_data()
    
    # Create output directory for plots
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'funnel_analysis')
    
    # Generate all funnel visualizations
    figs = {
        'overall': create_overall_funnel(df),
        'segment': create_segment_funnel(df),
        'region': create_region_funnel(df)
    }
    
    # Save all plots
    save_plots(figs, output_dir)
    
    print(f"\nFunnel analysis plots have been saved to: {output_dir}")
    print("Files generated:")
    print("- overall_funnel.html (interactive)")
    print("- segment_funnel.png")
    print("- region_funnel.png")
