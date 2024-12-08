import streamlit as st
import pandas as pd
import os

# Streamlit app starts here
st.title("Food Data Search Tool")

# Automatically load the CSV file from ./data directory
data_dir = "./data"
default_file_name = "index.csv"
file_path = os.path.join(data_dir, default_file_name)

if os.path.exists(file_path):
    # Load the CSV
    df = pd.read_csv(file_path)
    st.success(f"Auto-imported '{default_file_name}' from './data' directory.")

    # Display the first few rows of the dataset
    st.subheader("Uploaded Dataset")
    st.dataframe(df.head())

    # Columns for searching
    food_code_col = df.columns[0]  # 'Food Code; code'
    food_name_col = df.columns[1]  # 'Food Name; name'
    scientific_name_col = df.columns[2]  # 'Scientific Name; scie'
    local_name_col = df.columns[3]  # 'Local Name; lang'

    # Sidebar search options
    st.sidebar.header("Search Options")
    search_by = st.sidebar.radio(
        "Search By:",
        options=[
            "Food Code",
            "Food Name",
            "Scientific Name",
            "Local Name"
        ]
    )
    search_query = st.sidebar.text_input("Enter your search query:")

    # Filter the dataset based on the selected search option
    filtered_df = df.copy()
    if search_query:
        if search_by == "Food Code":
            filtered_df = filtered_df[
                filtered_df[food_code_col].str.contains(search_query, case=False, na=False)
            ]
        elif search_by == "Food Name":
            filtered_df = filtered_df[
                filtered_df[food_name_col].str.contains(search_query, case=False, na=False)
            ]
        elif search_by == "Scientific Name":
            filtered_df = filtered_df[
                filtered_df[scientific_name_col].str.contains(search_query, case=False, na=False)
            ]
        elif search_by == "Local Name":
            filtered_df = filtered_df[
                filtered_df[local_name_col].str.contains(search_query, case=False, na=False)
            ]

    # Display the search results
    st.subheader("Search Results")
    if not filtered_df.empty:
        for index, row in filtered_df.iterrows():
            st.write(f"### Food Details (Row {index + 1})")
            for col, value in row.items():
                st.write(f"**{col}**: {value}")
            st.markdown("---")
    else:
        st.warning("No results found for your search query.")
else:
    st.warning(
        f"No file found at '{file_path}'. Please place a CSV file named '{default_file_name}' in the './data' directory.")
