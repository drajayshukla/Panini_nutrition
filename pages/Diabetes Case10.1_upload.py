import streamlit as st
from fpdf import FPDF
import tempfile
import pandas as pd
import csv
import io

# Load symptoms and default responses from a CSV file
@st.cache
def load_symptoms_data(file):
    df = pd.read_csv(file)
    return df

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

# Upload the CSV file
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
            self.set_font("Arial", size=8)
            table_width = self.w - 20
            col_widths = [table_width * 0.4, table_width * 0.15, table_width * 0.45]
            row_height = 5

            self.set_fill_color(200, 200, 200)
            self.cell(col_widths[0], row_height, "Symptom", border=1, align='C', fill=True)
            self.cell(col_widths[1], row_height, "Response", border=1, align='C', fill=True)
            self.cell(col_widths[2], row_height, "Remark", border=1, align='C', fill=True)
            self.ln(row_height)

            for symptom, response in responses.items():
                if "_remark" not in symptom:
                    self.cell(col_widths[0], row_height, symptom, border=1)
                    if response.lower() == "yes":
                        self.set_fill_color(144, 238, 144)
                    elif response.lower() == "no":
                        self.set_fill_color(255, 182, 193)
                    else:
                        self.set_fill_color(173, 216, 230)
                    self.cell(col_widths[1], row_height, response, border=1, align='C', fill=True)

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
