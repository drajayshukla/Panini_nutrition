import streamlit as st
import pandas as pd

# Streamlit app starts here
st.title("Search and Divide Dataset")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load the CSV
    df = pd.read_csv(uploaded_file)

    # Display the first few rows of the dataset
    st.subheader("Uploaded Dataset")
    st.dataframe(df.head())

    # Columns for searching
    column_names = df.columns
    search_columns = {
        column_names[0]: "Code (Index 0)",
        column_names[1]: "Name (Index 1)",
        column_names[3]: "Language (Index 3)"
    }

    # Sidebar for search options
    st.sidebar.header("Search Options")
    selected_column = st.sidebar.selectbox("Select a column to search", list(search_columns.keys()))
    search_query = st.sidebar.text_input(f"Search by {search_columns[selected_column]}")

    # Filter the dataset based on the search
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df[selected_column].str.contains(search_query, case=False, na=False)
        ]

    # Display the filtered dataset
    st.subheader("Filtered Dataset")
    st.dataframe(filtered_df)

    # Provide download option for filtered data
    if not filtered_df.empty:
        st.download_button(
            label="Download Filtered Data",
            data=filtered_df.to_csv(index=False),
            file_name="filtered_data.csv",
            mime="text/csv",
        )
    else:
        st.warning("No results match your search query.")
else:
    st.warning("Please upload a CSV file to proceed.")
