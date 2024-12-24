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
# Function to process the uploaded file
def process_file(file_path, output_file_path='filtered_inlinks.xlsx'):
    # Read the file content
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

    # Define the status codes to filter out
    status_codes_to_filter = [0, 200, 204]

    # Filter out rows with specified status codes
    filtered_df = df[~df.iloc[:, 6].isin(status_codes_to_filter)]

    # Save the filtered data to a new Excel file
    filtered_df.to_excel(output_file_path, index=False)

    # Count URLs with specific status codes
    status_codes_to_count = [0, 401, 404, 403, 500, 502, 503, 504, 204, 301, 302, 303, 304]

    # Create a dictionary to store counts for each status code
    count_per_status_code = {code: len(filtered_df[filtered_df.iloc[:, 6] == code]) for code in status_codes_to_count}

    return filtered_df, count_per_status_code

# Function to create a bar chart
def create_bar_chart(count_per_status_code):
    plt.bar(count_per_status_code.keys(), count_per_status_code.values())
    plt.xlabel('Status Code')
    plt.ylabel('Number of URLs')
    plt.title('Number of URLs for Each Status Code')
    plt.show()

# Function to generate download link
def generate_download_link(file_path):
    with open(file_path, 'rb') as file:
        b64 = base64.b64encode(file.read()).decode()
    return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="filtered_inlinks.xlsx">Download filtered_inlinks.xlsx</a>'

# Main execution block
if __name__ == "__main__":
    # Input file path
    input_file_path = input("Enter the path to your file (CSV or XLSX): ")
    output_file_path = 'filtered_inlinks.xlsx'

    # Process the file
    filtered_df, count_per_status_code = process_file(input_file_path, output_file_path)

    # Print status code counts
    print("Number of internal links with Non-HTTP 2xx:")
    for code, count in count_per_status_code.items():
        print(f"Number of URLs with Status Code {code}: {count}")

    # Generate and display bar chart
    create_bar_chart(count_per_status_code)

    # Display filtered rows
    print("Filtered rows with Non-HTTP 2xx:")
    print(filtered_df.head())

    # Generate download link
    download_link = generate_download_link(output_file_path)
    print("Download link for filtered table:")
    print(download_link)
