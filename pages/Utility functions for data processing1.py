import streamlit as st
import pandas as pd
import numpy as np
import zipfile
import os

# Utility functions for data processing
def round_val(val):
    """Round value to 12 decimal places."""
    return np.round(val, 12)

def parse_value(val, factor, related_col=None, related_val=None):
    """
    Parse and transform value based on a factor and an optional related column.
    """
    if pd.isna(val):
        return 0
    val = float(val)
    factor = float(factor.split('*')[0])
    multiplier = float(related_val) if related_col and related_val else 1
    return round_val(val * factor * multiplier)

def process_data(raw_data, factors, renames, sums):
    """
    Process the raw data based on factors, renames, and sums.
    """
    # Create a dictionary to hold processed data
    processed_data = {col: [] for col in raw_data.columns}
    for index, row in raw_data.iterrows():
        for col in raw_data.columns:
            value = row[col]
            if col in factors:
                factor = factors[col]
                processed_value = parse_value(value, factor)
                processed_data[col].append(processed_value)
            else:
                processed_data[col].append(value)
    return pd.DataFrame(processed_data)

def load_csv_from_folder(folder_path, file_name):
    """
    Load a CSV file from the extracted folder.
    """
    file_path = os.path.join(folder_path, file_name)
    return pd.read_csv(file_path)

# Streamlit app starts here
st.title("Nutrition Dataset Processor")

# Upload ZIP folder
st.sidebar.header("Upload Folder as ZIP")
zip_file = st.sidebar.file_uploader("Upload a ZIP file containing all required CSV files", type=["zip"])

if zip_file:
    # Create a temporary folder to extract the zip file
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        temp_dir = "temp_extracted"
        zip_ref.extractall(temp_dir)

    # Load the required files from the extracted folder
    try:
        raw_data = load_csv_from_folder(temp_dir, "raw_data.csv")
        factors = load_csv_from_folder(temp_dir, "factors.csv").set_index('code')['factor'].to_dict()
        renames = load_csv_from_folder(temp_dir, "renames.csv").set_index('code')['actual'].to_dict()
        sums = load_csv_from_folder(temp_dir, "sums.csv").set_index('code')['expression'].to_dict()

        # Display the raw dataset
        st.subheader("Raw Dataset Preview")
        st.dataframe(raw_data.head())

        # Process the data
        st.subheader("Processing Data...")
        processed_data = process_data(raw_data, factors, renames, sums)
        st.success("Data processed successfully!")

        # Display processed data
        st.subheader("Processed Dataset")
        st.dataframe(processed_data.head())

        # Provide a download button for the processed CSV
        st.download_button(
            label="Download Processed Data",
            data=processed_data.to_csv(index=False),
            file_name="processed_data.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"An error occurred while processing: {e}")

    # Cleanup temporary directory after processing
    finally:
        if os.path.exists(temp_dir):
            for root, dirs, files in os.walk(temp_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(temp_dir)

else:
    st.warning("Please upload a ZIP folder containing all required CSV files.")

