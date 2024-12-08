import uuid
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

# Initialize DataFrame to store generated codes and details
if "generated_codes" not in st.session_state:
    st.session_state.generated_codes = pd.DataFrame(
        columns=["Name", "Purpose", "Unique Code", "Validity Days", "Expiration Date"])


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
    return new_entry


# Streamlit UI
st.title("Unique Code Generator")

# Input fields
name = st.text_input("Enter the name of the person")
purpose = st.text_input("Enter the purpose of the unique code")
validity_days = st.number_input("Enter the number of validity days", min_value=1, step=1)

# Generate button
if st.button("Generate Code"):
    if name and purpose and validity_days:
        entry = generate_and_save_code(name, purpose, validity_days)
        st.success("Unique Code Generated Successfully!")
        st.write(entry)
    else:
        st.error("Please fill in all fields!")

# Display generated codes
st.subheader("Generated Unique Codes")
st.dataframe(st.session_state.generated_codes)
