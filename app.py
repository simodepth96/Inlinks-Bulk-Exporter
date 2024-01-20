import streamlit as st
import pandas as pd
import plotly.express as px

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

    # Count the number of rows with specific status codes that are being removed
    count_per_status_code = {code: len(df[df.iloc[:, 6] == code]) for code in status_codes_to_filter}

    # Save the filtered data to a new Excel file
    filtered_df.to_excel('filtered_inlinks.xlsx', index=False)

    # Print out the number of rows removed for each status code
    for code, count in count_per_status_code.items():
        st.write(f"Number of rows removed with Status Code {code}: {count}")

    # Count URLs with specific status codes
    status_codes_to_count = [401, 404, 403, 500, 502, 503, 504, 204, 301, 302, 303, 304]

    # Create a dictionary to store counts for each status code
    count_per_status_code = {code: len(filtered_df[filtered_df.iloc[:, 6] == code]) for code in status_codes_to_count}

    # Print out the counts
    for code, count in count_per_status_code.items():
        st.write(f"Number of URLs with Status Code {code}: {count}")

    # Create a bar chart using Plotly Express
    fig = px.bar(x=list(count_per_status_code.keys()), y=list(count_per_status_code.values()),
                 labels={'x': 'Status Code', 'y': 'Number of URLs'},
                 title='Number of URLs for Each Status Code')

    # Show the chart
    st.plotly_chart(fig)
