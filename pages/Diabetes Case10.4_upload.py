import streamlit as st
from fpdf import FPDF
import tempfile
import pandas as pd
import csv
import io
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from PIL import Image
import os

# Initialize Google Drive authentication
def initialize_google_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto-authenticates
    return GoogleDrive(gauth)

# Load symptoms and default responses from a CSV file
@st.cache
def load_symptoms_data(file):
    df = pd.read_csv(file)
    return df

# Authenticate and initialize Google Sheets
def initialize_google_sheet():
    credentials_file = "wired-rex-384216-022ef0ae8b96.json"  # Replace with your credentials file
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(credentials)
    sheet = client.open("Symptom Checker Responses").sheet1
    return sheet

# Upload file to Google Drive
def upload_to_google_drive(drive, file_name, file_path):
    file_drive = drive.CreateFile({'title': file_name})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    return file_drive['alternateLink']

# Create a template CSV file
def generate_template_csv():
    template_data = {
        "Symptom": ["Fever", "Cough", "Headache"],
        "Default_Response": ["Other", "Yes", "No"]
    }
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["Symptom", "Default_Response"])
    writer.writeheader()
    for symptom, response in zip(template_data["Symptom"], template_data["Default_Response"]):
        writer.writerow({"Symptom": symptom, "Default_Response": response})
    return output.getvalue()

# Upload CSV and other files
st.title("Symptom Checker")
st.markdown(
    "### Instructions: \n"
    "1. Upload a CSV file with two columns: 'Symptom' and 'Default_Response'.\n"
    "2. Each symptom should have a default response: 'Yes', 'No', or 'Other'.\n"
    "3. If you're unsure about the format, download the template below."
)
st.download_button(
    label="Download Template CSV",
    data=generate_template_csv(),
    file_name="symptoms_template.csv",
    mime="text/csv",
)

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV file with symptoms and default responses", type=["csv"])

# Upload image or PDF
st.markdown("### Optional: Upload an image or PDF file (e.g., for reference)")
uploaded_image_or_pdf = st.file_uploader("Upload Image or PDF", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file:
    st.success("CSV file uploaded successfully! Please fill in the form below.")
    data = load_symptoms_data(uploaded_file)
    symptoms = data['Symptom'].tolist()
    default_responses = data.set_index('Symptom')['Default_Response'].to_dict()

    responses = {}

    # Input fields
    for symptom in symptoms:
        col1, col2, col3 = st.columns([2, 1.5, 4])
        with col1:
            st.write(symptom)
        with col2:
            default_value = default_responses.get(symptom, "Other")
            responses[symptom] = st.radio(
                f"Response for {symptom}",
                ["Other", "Yes", "No"],
                index=["Other", "Yes", "No"].index(default_value),
                key=symptom
            )
        with col3:
            responses[f"{symptom}_remark"] = st.text_input(
                f"Remarks for {symptom} (if any)", key=f"{symptom}_remark"
            )

    # Upload to Google Drive if a file is uploaded
    if uploaded_image_or_pdf:
        file_type = uploaded_image_or_pdf.type
        file_name = uploaded_image_or_pdf.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as temp_file:
            temp_file.write(uploaded_image_or_pdf.getbuffer())
            temp_file_path = temp_file.name

        # Initialize Google Drive
        drive = initialize_google_drive()

        # Upload file to Google Drive
        file_link = upload_to_google_drive(drive, file_name, temp_file_path)
        st.success(f"File uploaded to Google Drive! [View File]({file_link})")

    # Save data to Google Sheets
    if st.button("Save to Google Sheet"):
        try:
            sheet = initialize_google_sheet()
            data_rows = []
            for symptom in symptoms:
                response = responses.get(symptom, "Other")
                remark = responses.get(f"{symptom}_remark", "")
                data_rows.append([symptom, response, remark])
            for row in data_rows:
                sheet.append_row(row)
            st.success("Data saved to Google Sheet successfully!")
        except Exception as e:
            st.error(f"Error saving to Google Sheet: {e}")
