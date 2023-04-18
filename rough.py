import os
import streamlit as st
import pandas as pd
import zipfile

# Define a function to load the first DataFrame from a folder based on user input
def load_dataframe1(inputs):
    # Get a list of all CSV files in the data folder
    files = [f for f in os.listdir('data') if f.endswith('.csv')]
    
    # Load each CSV file into a DataFrame and concatenate them
    df = pd.concat([pd.read_csv(os.path.join('data', f)) for f in files])
    
    # Filter the DataFrame based on the user's input
    if inputs:
        df = df[df['column'].isin(inputs)]
    
    return df

# Define a function to load the second DataFrame from a folder based on user input
def load_dataframe2(inputs):
    # Get a list of all CSV files in the data2 folder
    files = [f for f in os.listdir('data2') if f.endswith('.csv')]
    
    # Load each CSV file into a DataFrame and concatenate them
    df = pd.concat([pd.read_csv(os.path.join('data2', f)) for f in files])
    
    # Filter the DataFrame based on the user's input
    if inputs:
        df = df[df['column'].isin(inputs)]
    
    return df

# Set the app title
st.title("My App")

# Add a sidebar with an input field for the first DataFrame
inputs1 = st.sidebar.text_input("Enter values separated by commas")
st.sidebar.subheader("Input Field 1")

# Add a sidebar with an input field for the second DataFrame
inputs2 = st.sidebar.text_input("Enter values separated by commas")
st.sidebar.subheader("Input Field 2")

# Load the first DataFrame based on the user's input, if given
if inputs1:
    df1 = load_dataframe1([x.strip() for x in inputs1.split(',')])
    st.write("First DataFrame")
    st.write(df1)
    
    # Add a button to download the first DataFrame, but only if inputs were given
    if st.button("Download First DataFrame"):
        with zipfile.ZipFile("first_dataframe.zip", "w") as zip:
            zip.writestr("first_dataframe.csv", df1.to_csv(index=False))
        st.markdown("Download the first DataFrame: [first_dataframe.zip](first_dataframe.zip)")

# Load the second DataFrame based on the user's input, if given
if inputs2:
    df2 = load_dataframe2([x.strip() for x in inputs2.split(',')])
    st.write("Second DataFrame")
    st.write(df2)
    
    # Add a button to download the second DataFrame, but only if inputs were given
    if st.button("Download Second DataFrame"):
        with zipfile.ZipFile("second_dataframe.zip", "w") as zip:
            zip.writestr("second_dataframe.csv", df2.to_csv(index=False))
        st.markdown("Download the second DataFrame: [second_dataframe.zip](second_dataframe.zip)")
