import streamlit as st
import pandas as pd

# Streamlit App Title
st.title("Upload CSV and Extract Specific Columns")

# Columns to keep (indices)
columns_to_keep = [
    0, 1, 2, 3, 4, 5, 6, 8, 10, 16, 20, 22, 24, 26,
    66, 68, 70, 76, 78, 100, 165, 170, 172, 178, 184, 194, 196, 200, 202
]

# Initialize session state for storing uploaded data
if "data" not in st.session_state:
    st.session_state["data"] = None

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the uploaded CSV file and update session state
        st.session_state["data"] = pd.read_csv(uploaded_file)

        # Ensure the selected indices exist in the dataset
        available_columns = [col for col in columns_to_keep if col < len(st.session_state["data"].columns)]

        # Extract specific columns
        extracted_df = st.session_state["data"].iloc[:, available_columns]

        # Display the new sub-database
        st.subheader("Extracted Columns Sub-database")
        st.write(extracted_df.head())  # Show the first few rows

        # Provide download option
        st.download_button(
            label="Download Sub-database CSV",
            data=extracted_df.to_csv(index=False),
            file_name="subdatabase.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    # Clear session state when no file is uploaded
    st.session_state["data"] = None
    st.info("Please upload a CSV file to proceed.")
