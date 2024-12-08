import streamlit as st
import pandas as pd

# Streamlit app starts here
st.title("Divide Dataset by Food Group")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load the CSV
    df = pd.read_csv(uploaded_file)

    # Display the first few rows of the dataset
    st.subheader("Uploaded Dataset")
    st.dataframe(df.head())

    # Ensure column index 4 (Food Group) is valid
    column_to_group = df.columns[4]
    st.write(f"Dividing data based on the column: **{column_to_group}**")

    # Divide the dataset based on the values in column index 4
    grouped_data = {group: group_df for group, group_df in df.groupby(column_to_group)}

    # Display groups and data
    for group, group_df in grouped_data.items():
        st.subheader(f"Food Group: {group}")
        st.dataframe(group_df)

        # Download button for each group
        csv_data = group_df.to_csv(index=False)
        st.download_button(
            label=f"Download {group} Data",
            data=csv_data,
            file_name=f"{group}_data.csv",
            mime="text/csv"
        )
else:
    st.warning("Please upload a CSV file to proceed.")
