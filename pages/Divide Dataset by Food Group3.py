import streamlit as st
import pandas as pd

# Streamlit app starts here
st.title("Food Data Search Tool")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load the CSV
    df = pd.read_csv(uploaded_file)

    # Display the first few rows of the dataset
    st.subheader("Uploaded Dataset")
    st.dataframe(df.head())

    # Columns for searching
    food_code_col = df.columns[0]  # 'Food Code; code'
    food_name_col = df.columns[1]  # 'Food Name; name'
    scientific_name_col = df.columns[2]  # 'Scientific Name; scie'

    # Sidebar search options
    st.sidebar.header("Search Options")
    search_by = st.sidebar.radio(
        "Search By:",
        options=[
            "Food Code",
            "Food Name",
            "Scientific Name"
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

    # Display the search results
    st.subheader("Search Results")
    if not filtered_df.empty:
        st.dataframe(filtered_df)

        # Provide download option for the filtered data
        st.download_button(
            label="Download Search Results",
            data=filtered_df.to_csv(index=False),
            file_name="search_results.csv",
            mime="text/csv",
        )
    else:
        st.warning("No results found for your search query.")
else:
    st.warning("Please upload a CSV file to proceed.")
