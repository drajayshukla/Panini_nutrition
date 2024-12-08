import streamlit as st
import pandas as pd

# Streamlit App Title
st.title("Upload and View CSV File")

# Upload CSV File
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

        # Display DataFrame
        st.subheader("Preview of the Uploaded CSV File")
        st.write(df.head())  # Show the first 5 rows of the data

        # Option to display full data
        if st.checkbox("Show full data"):
            st.write(df)

        # Show DataFrame Statistics
        st.subheader("Basic DataFrame Information")
        st.write(f"Number of Rows: {df.shape[0]}")
        st.write(f"Number of Columns: {df.shape[1]}")
        st.write("Column Names:", list(df.columns))

        # Data Types
        st.subheader("Data Types")
        st.write(df.dtypes)

    except Exception as e:
        st.error(f"Error while loading CSV: {e}")
else:
    st.info("Please upload a CSV file to proceed.")
