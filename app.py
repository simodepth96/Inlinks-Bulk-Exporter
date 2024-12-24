import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# Streamlit UI
st.title("Broken Inlinks Bulk Exporter")

# Sidebar
st.sidebar.header("🔧 How to use?")
st.sidebar.markdown(
    """
    - Screaming Frog > Bulk Exports > Links > All Inlinks
    - Upload an XLSX/CSV file.
    """
    )
# Use cases - subheader
st.sidebar.subheader(
        "🎯 Features"
    )
st.sidebar.markdown(
    """
1. Filters out the rows with valid URLs (HTTP 2xx)\n
2. Counts how many internal links with adverse status code (Non-HTTP 2xx)\n
3. Plots a distribution of most common status codes\n
4. Provides a cleaned table with broken internal links\n
"""
    )

# File upload
file = st.file_uploader("Upload XLSX or CSV file with the Screaming Frog export file", type=["xlsx", "csv"])

if file is not None:
    st.write("File Uploaded Successfully!")

    # Read the file content
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    # Define the status codes to filter out
    status_codes_to_filter = [0, 200, 204]

    # Filter out rows with specified status codes
    filtered_df = df[~df.iloc[:, 6].isin(status_codes_to_filter)]

    # Count the number of rows with specific status codes that are being removed
    count_per_status_code = {code: len(df[df.iloc[:, 6] == code]) for code in status_codes_to_filter}

    # Save the filtered data to a new Excel file
    output_file_path = 'filtered_inlinks.xlsx'
    filtered_df.to_excel(output_file_path, index=False)

    # Count URLs with specific status codes
    status_codes_to_count = [0, 401, 404, 403, 500, 502, 503, 504, 204, 301, 302, 303, 304]

    # Create a dictionary to store counts for each status code
    count_per_status_code = {code: len(filtered_df[filtered_df.iloc[:, 6] == code]) for code in status_codes_to_count}

    st.markdown("## Number of internal links with Non-HTTP 2xx")

    # Print out the counts
    for code, count in count_per_status_code.items():
        st.write(f"Number of URLs with Status Code {code}: {count}")
        
        fig, ax = plt.subplots()
        ax.bar(count_per_status_code.keys(), count_per_status_code.values())
        ax.set_xlabel('Status Code')
        ax.set_ylabel('Number of URLs')

    # Display the chart in Streamlit
    st.write("## Distribution of Non-Valid Status Codes")
    st.pyplot(fig)

    # Display the table with filtered rows
    st.write("## Table with Non-HTTP 2xx inlinks:")
    st.dataframe(filtered_df)

    # Download link for filtered table
    st.markdown("### Download Filtered Table")
    st.markdown(f"Click the link below to download the table with Non-HTTP 2xx inlinks")
    st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{base64.b64encode(open(output_file_path, "rb").read()).decode()}" download="filtered_inlinks.xlsx">Download filtered_inlinks.xlsx</a>', unsafe_allow_html=True)
