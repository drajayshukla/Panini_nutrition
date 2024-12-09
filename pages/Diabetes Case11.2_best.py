import streamlit as st
import streamlit as st

from fpdf import FPDF
import tempfile
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Hardcoded credentials (username: password)
USERNAME = "admin"
PASSWORD = "password123"

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

# Define the login screen
def login_screen():
    st.title("Login")
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    if st.button("Login"):
        if username_input == USERNAME and password_input == PASSWORD:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username_input
        else:
            st.error("Invalid username or password. Please try again.")

# Define the main app content
def main_app():
    st.success(f"Welcome, {st.session_state['username']}! You are logged in.")

    # Logout button
    if st.button("Log Out"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None

    # Main app content goes here
    st.write("This is your main app content. Add your algorithm below!")
    st.write("Welcome to the Symptom Checker App!")

    def connect_to_google_sheet(sheet_name):
        try:
            # Define the scope for Google Sheets and Drive API
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

            # Load credentials from the JSON key file
            creds = ServiceAccountCredentials.from_json_keyfile_name("../storage/wired-rex-384216-022ef0ae8b96.json", scope)

            # Authorize the client
            client = gspread.authorize(creds)

            # Open the specified sheet
            spreadsheet = client.open(sheet_name)
            st.success(f"Connected to Google Sheets: {sheet_name}")
            return spreadsheet.sheet1
        except gspread.SpreadsheetNotFound:
            st.warning(f"Google Sheet '{sheet_name}' not found. Attempting to connect to the backup sheet...")
            return None
        except FileNotFoundError:
            st.error("JSON credentials file not found. Please ensure the file is in the working directory.")
        except gspread.exceptions.APIError as api_error:
            st.error(f"API Error: {api_error}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
        return None

    # Connect to Primary and Backup Google Sheets
    primary_sheet_name = "Diabetes_case_10.1_best"
    backup_sheet_name = "Backup_Diabetes_Cases"

    sheet = connect_to_google_sheet(primary_sheet_name)
    if not sheet:
        st.warning("Switching to backup sheet...")
        sheet = connect_to_google_sheet(backup_sheet_name)

    # Load symptoms and default responses from a CSV file
    @st.cache
    def load_symptoms_data():
        file_path = "data/casesheetDM.csv"
        df = pd.read_csv(file_path)
        return df

    # Main app
    st.title("Symptom Checker with Google Sheets Backup")

    try:
        # Load symptoms data
        data = load_symptoms_data()
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

        # PDF generation class
        class EnhancedPDF(FPDF):
            def header(self):
                self.set_font("Arial", size=10, style="B")
                self.cell(0, 10, "Symptom Checker Report", ln=True, align='C')
                self.ln(5)

            def add_colored_symptom_table(self, responses):
                self.set_font("Arial", size=8)
                table_width = self.w - 20
                col_widths = [table_width * 0.4, table_width * 0.15, table_width * 0.45]
                row_height = 5

                # Table header
                self.set_fill_color(200, 200, 200)
                self.cell(col_widths[0], row_height, "Symptom", border=1, align='C', fill=True)
                self.cell(col_widths[1], row_height, "Response", border=1, align='C', fill=True)
                self.cell(col_widths[2], row_height, "Remark", border=1, align='C', fill=True)
                self.ln(row_height)

                # Table rows
                for symptom, response in responses.items():
                    if "_remark" not in symptom:
                        self.cell(col_widths[0], row_height, symptom, border=1)

                        # Color-coded response column
                        if response.lower() == "yes":
                            self.set_fill_color(144, 238, 144)
                        elif response.lower() == "no":
                            self.set_fill_color(255, 182, 193)
                        else:
                            self.set_fill_color(173, 216, 230)
                        self.cell(col_widths[1], row_height, response, border=1, align='C', fill=True)

                        # Wrap remarks in the remark column
                        remark_key = f"{symptom}_remark"
                        remark = responses.get(remark_key, "")
                        self.multi_cell(col_widths[2], row_height, remark, border=1)
                        self.ln(0)

        def generate_enhanced_pdf(responses):
            pdf = EnhancedPDF()
            pdf.set_auto_page_break(auto=True, margin=10)
            pdf.add_page()
            pdf.add_colored_symptom_table(responses)
            return pdf

        # Save responses to Google Sheets
        # Save responses to Google Sheets
        # Save responses to Google Sheets
        # Save responses to Google Sheets
        if st.button("Save to Google Sheet"):
            if sheet:
                try:
                    # Prepare data for Google Sheets
                    sheet_data = [[symptom, responses[symptom], responses.get(f"{symptom}_remark", "")]
                                  for symptom in symptoms]

                    # Add headers only if the sheet is empty
                    existing_data = sheet.get_all_values()  # Fetch all existing data
                    if not existing_data:  # Add headers only if the sheet is empty
                        headers = [["Symptom", "Response", "Remark"]]
                        sheet.append_rows(headers)

                    # Batch append rows to Google Sheet
                    sheet.append_rows(sheet_data)
                    st.success("Responses saved to Google Sheet successfully!")
                except gspread.exceptions.APIError as api_error:
                    st.error(f"Google Sheets API Error: {api_error}")
                except Exception as e:
                    st.error(f"Error saving to Google Sheet: {e}")
            else:
                st.error("Google Sheet connection is not available. Please check your connection.")

        # View Google Sheet content
        if st.button("View Google Sheet Content"):
            if sheet:
                try:
                    # Fetch all data from the Google Sheet
                    data = sheet.get_all_records()  # Get all rows as a list of dictionaries
                    if data:
                        # Convert to a DataFrame for display
                        df = pd.DataFrame(data)
                        st.write("Current Google Sheet Data:")
                        st.dataframe(df)  # Display the sheet data in a table
                    else:
                        st.warning("No data found in the Google Sheet.")
                except gspread.exceptions.APIError as api_error:
                    st.error(f"Google Sheets API Error: {api_error}")
                except Exception as e:
                    st.error(f"Error fetching Google Sheet content: {e}")
            else:
                st.error("Google Sheet connection is not available. Please check your connection.")

        # Generate and download PDF
        if st.button("Generate Enhanced PDF"):
            pdf = generate_enhanced_pdf(responses)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                pdf_path = tmp_file.name
                pdf.output(pdf_path)

            st.success("PDF generated successfully!")
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="Download Enhanced PDF",
                    data=file,
                    file_name="Symptom_Report.pdf",
                    mime="application/pdf",
                )

    except FileNotFoundError:
        st.error(
            "The required CSV file (casesheetDM.csv) was not found in the 'data' folder. Please ensure the file exists.")

if st.session_state["logged_in"]:
    main_app()
else:
    login_screen()


















