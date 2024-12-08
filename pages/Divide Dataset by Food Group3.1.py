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

    # Nutrient selection options
    st.sidebar.header("Select Nutrient Columns")
    nutrient_columns = list(df.columns[4:])  # Assuming nutrients start from column 5

    # Default nutrients
    default_nutrients = ["Energy", "Protein"]
    optional_nutrients = [col for col in nutrient_columns if col not in default_nutrients]

    selected_nutrients = default_nutrients.copy()
    for nutrient in optional_nutrients:
        if st.sidebar.checkbox(f"Include {nutrient}", value=False):
            selected_nutrients.append(nutrient)

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

    # Display the specific entry with selected nutrients
    if not filtered_df.empty:
        st.subheader("Search Result")
        # Display only the first match
        row = filtered_df.iloc[0]
        for col, value in row.items():
            if col in [food_code_col, food_name_col, scientific_name_col, local_name_col] or col in selected_nutrients:
                st.write(f"**{col}**: {value}")
    else:
        st.warning("No results found for your search query.")
else:
    st.warning(
        f"No file found at '{file_path}'. Please place a CSV file named '{default_file_name}' in the './data' directory.")
