import pandas as pd

def replace_invalid_dates(df: pd.DataFrame, date_column: str, max_valid_date: str):
    # Convert the date column to datetime, setting errors='coerce' to handle invalid dates
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    
    # Define the maximum valid date
    max_valid_date = pd.to_datetime(max_valid_date)
    
    # Replace dates greater than the maximum valid date with the maximum valid date
    df.loc[df[date_column] > max_valid_date, date_column] = max_valid_date
    
    # Convert the datetime column back to string format
    df[date_column] = df[date_column].dt.strftime('%Y-%m-%d')
    
    return df

if __name__ == "__main__":
    # Sample data
    data = {
        'date_column': ['2025-01-01', '2999-12-31', '2262-04-10', '2262-04-12']
    }
    df = pd.DataFrame(data)
    
    # Replace invalid dates
    df = replace_invalid_dates(df, 'date_column', '2262-04-11')
    
    print(df)
