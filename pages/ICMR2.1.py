import streamlit as st
import pandas as pd

# Streamlit App Title
st.title("Upload, Process, and View CSV File")

# Upload CSV File
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

        # Multiply column at index 7 by 0.239 and add new column 'Energy kcal' at index 8
        if len(df.columns) > 7:  # Ensure the 7th index exists
            df.insert(8, "Energy kcal", df.iloc[:, 7] * 0.239)
            st.success("'Energy kcal' column successfully added.")
        else:
            st.error("The CSV file must have at least 8 columns for this operation.")

        # Display DataFrame
        st.subheader("Preview of the Processed CSV File")
        st.write(df.head())  # Show the first 5 rows of the processed data

        # Option to download processed file
        st.download_button(
            label="Download Processed CSV",
            data=df.to_csv(index=False),
            file_name="processed_data.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Error while processing the CSV: {e}")
else:
    st.info("Please upload a CSV file to proceed.")
