import uuid
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import os

# File to store data persistently
DATA_FILE = "generated_codes.csv"


# Initialize DataFrame
def load_data():
    """Load data from a file or initialize an empty DataFrame."""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Purpose", "Unique Code", "Validity Days", "Expiration Date"])


def save_data(data):
    """Save the DataFrame to a file."""
    data.to_csv(DATA_FILE, index=False)


# Load existing data
if "generated_codes" not in st.session_state:
    st.session_state.generated_codes = load_data()


def generate_and_save_code(name, purpose, validity_days):
    """
    Generates a unique alphanumeric code with an expiration date, saves the code with additional details.

    Args:
        name (str): Name of the person.
        purpose (str): Purpose of the unique code.
        validity_days (int): Number of validity days.

    Returns:
        dict: Generated code details.
    """
    # Generate a unique alphanumeric code
    unique_code = uuid.uuid4().hex.upper()[:8]  # Truncated to 8 characters for brevity

    # Calculate expiration date
    expiration_date = datetime.now() + timedelta(days=validity_days)
    expiration_date_str = expiration_date.strftime('%Y-%m-%d %H:%M:%S')

    # Save details in the DataFrame
    new_entry = {
        "Name": name,
        "Purpose": purpose,
        "Unique Code": unique_code,
        "Validity Days": validity_days,
        "Expiration Date": expiration_date_str
    }
    st.session_state.generated_codes = pd.concat(
        [st.session_state.generated_codes, pd.DataFrame([new_entry])], ignore_index=True
    )
    save_data(st.session_state.generated_codes)  # Save to file
    return new_entry


def check_code_validity_with_details(code):
    """
    Checks the validity of a given unique code and provides full details.

    Args:
        code (str): The unique code to check.

    Returns:
        dict or str: Full details if the code is found, otherwise a message indicating the code was not found.
    """
    # Search for the code in the DataFrame
    codes_df = st.session_state.generated_codes
    if code in codes_df["Unique Code"].values:
        code_details = codes_df[codes_df["Unique Code"] == code].iloc[0]
        expiration_date = datetime.strptime(code_details["Expiration Date"], '%Y-%m-%d %H:%M:%S')
        is_valid = datetime.now() <= expiration_date
        validity_status = "VALID" if is_valid else "EXPIRED"

        # Return full details
        return {
            "Name": code_details["Name"],
            "Purpose": code_details["Purpose"],
            "Unique Code": code_details["Unique Code"],
            "Validity Days": code_details["Validity Days"],
            "Expiration Date": code_details["Expiration Date"],
            "Status": validity_status
        }
    else:
        return f"The code '{code}' was NOT FOUND."


# Streamlit UI
st.title("Unique Code Generator and Validator")

# Option selection
option = st.radio("Choose an option:", ["Generate New Code", "Check Code Validity"])

if option == "Generate New Code":
    st.header("Generate a Unique Code")
    name = st.text_input("Enter the name of the person")
    purpose = st.text_input("Enter the purpose of the unique code")
    validity_days = st.number_input("Enter the number of validity days", min_value=1, step=1)

    if st.button("Generate Code"):
        if name and purpose and validity_days:
            entry = generate_and_save_code(name, purpose, validity_days)
            st.success("Unique Code Generated Successfully!")
            st.write(entry)
        else:
            st.error("Please fill in all fields!")

elif option == "Check Code Validity":
    st.header("Check Code Validity")
    code_to_check = st.text_input("Enter the unique code to check its validity")
    if st.button("Check Code"):
        if code_to_check:
            result = check_code_validity_with_details(code_to_check)
            if isinstance(result, dict):
                st.success(
                    f"The code '{result['Unique Code']}' is {result['Status']} until {result['Expiration Date']}.")
                st.write("Full Details:")
                st.write(result)
            else:
                st.error(result)
        else:
            st.error("Please enter a unique code to check!")
