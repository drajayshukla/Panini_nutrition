import streamlit as st
from fpdf import FPDF

# Function to generate PDF
def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for section, details in data.items():
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt=section, ln=True, align="L")
        pdf.set_font("Arial", size=12)
        for key, value in details.items():
            pdf.multi_cell(0, 10, txt=f"{key}: {value}")
        pdf.ln()
    return pdf

# Streamlit App
st.title("Medical History and Examination")

# Sections for user input
sections = {
    "Previous Illness": {
        "Diabetes Mellitus": st.checkbox("Diabetes Mellitus"),
        "Hypertension": st.checkbox("Hypertension"),
        "Coronary Artery Disease": st.checkbox("Coronary Artery Disease"),
        "Peripheral Vascular Disease": st.checkbox("Peripheral Vascular Disease"),
        "Diabetic Retinopathy": st.checkbox("Diabetic Retinopathy"),
    },
    "Lifestyle": {
        "Smoking": st.radio("Smoking", ["Yes", "No"]),
        "Alcohol": st.radio("Alcohol", ["Yes", "No"]),
        "Exercise": st.selectbox("Exercise Level", ["Poor", "Average", "Good"]),
    },
    "Current Treatment": {
        "Type of Insulin": st.selectbox(
            "Type of Insulin", ["None", "Premixed", "Analog", "Mixed"]
        ),
        "Diet Compliance": st.selectbox(
            "Diet Compliance", ["Poor", "Average", "Good"]
        ),
    },
    "Measurements": {
        "Weight (kg)": st.text_input("Weight (kg)"),
        "Blood Glucose (mg/dL)": st.text_input("Blood Glucose (mg/dL)"),
    },
    "General Examination": {
        "Pallor": st.radio("Pallor", ["Yes", "No"]),
        "Edema": st.radio("Edema", ["Yes", "No"]),
    },
}

# Create PDF button
if st.button("Generate PDF"):
    # Collect data
    collected_data = {}
    for section, fields in sections.items():
        collected_data[section] = {k: v for k, v in fields.items()}

    # Create and save PDF
    pdf = create_pdf(collected_data)
    pdf_file = "/tmp/medical_summary.pdf"
    pdf.output(pdf_file)

    # Make it downloadable
    with open(pdf_file, "rb") as file:
        st.download_button(
            label="Download PDF",
            data=file,
            file_name="medical_summary.pdf",
            mime="application/pdf",
        )
