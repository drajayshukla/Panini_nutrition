import streamlit as st
from fpdf import FPDF
from PIL import Image

# App title
st.title("Pediatric Obesity Evaluation (Child < 5 Years)")

# Section: Patient Summary
st.header("Patient Summary")
name = st.text_input("Name")
age = st.number_input("Age (in years)", min_value=0.0, max_value=5.0, step=0.1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
height = st.number_input("Height/Length (cm)", min_value=0.0, step=0.1)
bmi = round(weight / ((height / 100) ** 2), 2) if height > 0 else 0.0
head_circumference = st.number_input("Head Circumference (cm)", min_value=0.0, step=0.1)

# Display calculated BMI
st.write(f"**Calculated BMI:** {bmi} kg/m²")

# General details
st.header("General Information")
par_consang = st.radio("Parental Consanguinity", ["Yes", "No"])
family_history = st.radio("Family History of Obesity", ["Yes", "No"])
gestational_age = st.text_input("Gestational Age (weeks)")
birth_weight = st.number_input("Birth Weight (kg)", min_value=0.0, step=0.1)
feeding_history = st.radio("Feeding History", ["Breastfed", "Formula-fed", "Mixed"])
milestones = st.radio("Developmental Milestones", ["Achieved", "Delayed"])

# Clinical evaluation
st.header("Clinical Evaluation")
remarks_dict = {}

# Signs and symptoms
st.subheader("Signs and Symptoms")
with st.expander("General Appearance"):
    central_obesity = st.checkbox("Central Obesity")
    remarks_dict["Central Obesity"] = st.text_area("Remarks for Central Obesity", key="remark_central_obesity")
    dysmorphic_features = st.checkbox("Dysmorphic Features")
    remarks_dict["Dysmorphic Features"] = st.text_area("Remarks for Dysmorphic Features", key="remark_dysmorphic_features")

# Repeat for other sections as needed
# Adding for brevity here; repeat this pattern for all symptoms and checkboxes
# ...

# Clinical notes
st.header("Clinical Notes")
clinical_notes = st.text_area("Enter additional clinical notes here")

# Picture upload
st.header("Picture Upload")
uploaded_image = st.file_uploader("Upload a picture (optional)", type=["png", "jpg", "jpeg"])

# Investigations
st.header("Investigations")
investigations = []
cbc = st.checkbox("Complete Blood Count (CBC)")
if cbc:
    investigations.append("Complete Blood Count (CBC)")
fbglucose = st.checkbox("Fasting Blood Glucose (FBG)")
if fbglucose:
    investigations.append("Fasting Blood Glucose (FBG)")

# Add other investigation checkboxes and append to the `investigations` list
# ...

# Red Flag Signs
st.header("Red Flag Signs")
red_flags = st.multiselect(
    "Red Flags",
    [
        "Severe developmental delay or regression",
        "Early-onset obesity (<2 years)",
        "Dysmorphic features",
        "Hyperphagia with constant seeking of food",
        "Rapid weight gain with height stunting",
        "Hypotonia",
        "Signs of endocrinopathy",
        "Family history of genetic disorders"
    ]
)

# Function to generate a PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Pediatric Obesity Evaluation Report', border=False, ln=True, align='C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, border=False, ln=True)
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_pdf(patient_data, red_flags, investigations, plan, clinical_notes, remarks, image_path=None):
    pdf = PDF()
    pdf.add_page()

    # Patient Summary
    pdf.chapter_title("Patient Summary")
    summary = "\n".join([f"{key}: {value}" for key, value in patient_data.items()])
    pdf.chapter_body(summary)

    # Red Flag Signs
    pdf.chapter_title("Red Flag Signs Identified")
    pdf.chapter_body(", ".join(red_flags) if red_flags else "None")

    # Investigations
    pdf.chapter_title("Investigations Ordered")
    pdf.chapter_body(", ".join(investigations) if investigations else "None")

    # Remarks
    pdf.chapter_title("Remarks for Symptoms")
    for symptom, remark in remarks.items():
        pdf.chapter_body(f"{symptom}: {remark if remark.strip() else 'No remarks provided'}")

    # Clinical Notes
    pdf.chapter_title("Clinical Notes")
    pdf.chapter_body(clinical_notes)

    # Plan of Management
    pdf.chapter_title("Plan of Management")
    pdf.chapter_body("\n".join(plan))

    # Picture
    if image_path:
        pdf.add_page()
        pdf.chapter_title("Uploaded Picture")
        pdf.image(image_path, x=10, y=50, w=180)

    # Save to buffer
    pdf_output = "Pediatric_Obesity_Evaluation_Report.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Streamlit app section for generating and downloading the PDF
if st.button("Download Report as PDF"):
    patient_data = {
        "Name": name,
        "Age": f"{age} years",
        "Gender": gender,
        "Weight": f"{weight} kg",
        "Height": f"{height} cm",
        "BMI": f"{bmi} kg/m²",
        "Head Circumference": f"{head_circumference} cm"
    }

    # Plan of Management
    plan = [
        "- Lifestyle interventions: Diet and physical activity counseling",
        "- Medical interventions: Based on underlying cause",
        "- Referral to specialist if needed"
    ]

    # Handle uploaded image
    image_path = None
    if uploaded_image:
        image = Image.open(uploaded_image)
        image_path = "uploaded_image.jpg"
        image.save(image_path)

    # Generate PDF
    pdf_file = generate_pdf(patient_data, red_flags, investigations, plan, clinical_notes, remarks_dict, image_path)

    # Provide download button
    with open(pdf_file, "rb") as pdf:
        st.download_button(
            label="Download PDF",
            data=pdf,
            file_name="Pediatric_Obesity_Evaluation_Report.pdf",
            mime="application/pdf"
        )
