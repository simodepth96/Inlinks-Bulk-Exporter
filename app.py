import streamlit as st
import pandas as pd
import plotly.express as px
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

    # Count the number of rows with specific status codes that are being removed
    count_per_status_code = {code: len(df[df.iloc[:, 6] == code]) for code in status_codes_to_filter}

    # Save the filtered data to a new Excel file
    output_file_path = 'filtered_inlinks.xlsx'
    filtered_df.to_excel(output_file_path, index=False)
    
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

    # Display the table with filtered rows
    st.write("Table containing Status Code that does not have 200 and 204:")
    st.dataframe(filtered_df)

    # Download link for filtered table
    st.markdown("### Download Filtered Table")
    st.markdown(f"Click the link below to download the table without Status Codes 200 and 204.")
    st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{base64.b64encode(open(output_file_path, "rb").read()).decode()}" download="filtered_inlinks.xlsx">Download filtered_inlinks.xlsx</a>', unsafe_allow_html=True)
