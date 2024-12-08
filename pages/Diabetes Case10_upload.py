import streamlit as st
from fpdf import FPDF
import tempfile
import pandas as pd


# Load symptoms and default responses from a CSV file
@st.cache
def load_symptoms_data(file):
    df = pd.read_csv(file)
    return df


# Upload the CSV file
st.title("Symptom Checker")
uploaded_file = st.file_uploader("Upload CSV file with symptoms and default responses", type=["csv"])

if uploaded_file:
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


    # PDF generation class
    class EnhancedPDF(FPDF):
        def header(self):
            self.set_font("Arial", size=10, style="B")
            self.cell(0, 10, "Symptom Checker Report", ln=True, align='C')
            self.ln(5)

        def add_colored_symptom_table(self, responses):
            self.set_font("Arial", size=8)  # Reduced font size
            table_width = self.w - 20  # Adjust margins
            col_widths = [table_width * 0.4, table_width * 0.15, table_width * 0.45]
            row_height = 5  # Reduced row height

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
                        self.set_fill_color(144, 238, 144)  # Light green
                    elif response.lower() == "no":
                        self.set_fill_color(255, 182, 193)  # Light red
                    else:
                        self.set_fill_color(173, 216, 230)  # Light blue
                    self.cell(col_widths[1], row_height, response, border=1, align='C', fill=True)

                    # Wrap remarks in the remark column
                    remark_key = f"{symptom}_remark"
                    remark = responses.get(remark_key, "")
                    self.multi_cell(col_widths[2], row_height, remark, border=1)
                    self.ln(0)  # Prevent double spacing


    def generate_enhanced_pdf(responses):
        pdf = EnhancedPDF()
        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.add_page()
        pdf.add_colored_symptom_table(responses)
        return pdf


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
else:
    st.info("Please upload a CSV file to proceed.")
