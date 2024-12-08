import streamlit as st
import pandas as pd
import numpy as np

# Utility functions for data processing
def round_val(val):
    """Round value to 12 decimal places."""
    return np.round(val, 12)

def significant_digits(n):
    """Calculate significant digits of a number."""
    return len(f"{n:.12e}".split('e')[0].replace('.', '').strip('0'))

def load_csv(file):
    """Load a CSV file."""
    return pd.read_csv(file)

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

# Streamlit app starts here
st.title("Nutrition Dataset Processor")

# Upload files
st.sidebar.header("Upload Files")
raw_file = st.sidebar.file_uploader("Upload Raw Dataset (CSV)", type=["csv"])
factors_file = st.sidebar.file_uploader("Upload Factors (CSV)", type=["csv"])
renames_file = st.sidebar.file_uploader("Upload Renames (CSV)", type=["csv"])
sums_file = st.sidebar.file_uploader("Upload Sums (CSV)", type=["csv"])

if raw_file and factors_file and renames_file and sums_file:
    # Load datasets
    raw_data = load_csv(raw_file)
    factors = load_csv(factors_file).set_index('code')['factor'].to_dict()
    renames = load_csv(renames_file).set_index('code')['actual'].to_dict()
    sums = load_csv(sums_file).set_index('code')['expression'].to_dict()

    # Process the raw data
    st.subheader("Raw Dataset Preview")
    st.dataframe(raw_data.head())

    st.subheader("Processing Data...")
    processed_data = process_data(raw_data, factors, renames, sums)
    st.success("Data processed successfully!")

    # Display processed data
    st.subheader("Processed Dataset")
    st.dataframe(processed_data.head())

    # Download the processed data
    st.download_button(
        label="Download Processed Data",
        data=processed_data.to_csv(index=False),
        file_name="processed_data.csv",
        mime="text/csv",
    )
else:
    st.warning("Please upload all required files to proceed.")

