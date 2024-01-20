import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import base64

# Streamlit UI
st.title("Export non-HTTP 2xx inlinks")

# File upload
file = st.file_uploader("Upload XLSX or CSV file", type=["xlsx", "csv"])

if file is not None:
    st.write("File Uploaded Successfully!")

    # Read the file content
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    # Display file content
    st.dataframe(df)

    # Define the status codes to filter out
    status_codes_to_filter = [200, 204]

    # Filter out rows with specified status codes
    filtered_df = df[~df.iloc[:, 6].isin(status_codes_to_filter)]

    # Display the table with filtered rows
    st.write("Table containing Status Code that does not have 200 and 204:")
    st.dataframe(filtered_df)

