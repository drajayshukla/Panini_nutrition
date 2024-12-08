import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Functions for calculations
def calculate_fat_mass(bmi, age, sex):
    return (1.2 * bmi) + (0.23 * age) - (10.8 * sex) - 5.4

def calculate_fat_free_mass(body_weight, fat_mass):
    return body_weight - fat_mass

def calculate_ffmi(fat_free_mass, height_m):
    return fat_free_mass / (height_m ** 2)

def calculate_body_fat_percentage(bmi, age, sex):
    if sex == 1:  # Male
        return (1.20 * bmi) + (0.23 * age) - 16.2
    else:  # Female
        return (1.20 * bmi) + (0.23 * age) - 5.4

def calculate_body_fat_siri(density):
    return (4.95 / density - 4.50) * 100

def calculate_body_density_3_site(sex, sum_skinfolds, age):
    if sex == 1:  # Male
        return 1.10938 - (0.0008267 * sum_skinfolds) + (0.0000016 * sum_skinfolds**2) - (0.0002574 * age)
    else:
        return 1.0994921 - (0.0009929 * sum_skinfolds) + (0.0000023 * sum_skinfolds**2) - (0.0001392 * age)

def calculate_body_density_7_site(sex, sum_skinfolds, age):
    return calculate_body_density_3_site(sex, sum_skinfolds, age)

# PDF generation function
def create_pdf(data, formulas, references):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Body Composition Report")
    c.line(100, 745, 500, 745)

    y = 720
    c.drawString(100, y, "Results:")
    y -= 20
    for key, value in data.items():
        c.drawString(100, y, f"{key}: {value}")
        y -= 20

    y -= 20
    c.drawString(100, y, "Formulas:")
    y -= 20
    for formula in formulas:
        c.drawString(100, y, formula)
        y -= 20

    y -= 20
    c.drawString(100, y, "References:")
    y -= 20
    for ref in references:
        c.drawString(100, y, ref)
        y -= 20

    c.save()
    buffer.seek(0)
    return buffer

# Streamlit app
st.title("Comprehensive Body Composition Calculator")
st.write("Calculate fat mass, fat-free mass, FFMI, body fat percentage, and Jackson-Pollock body fat using validated methods.")

# User inputs
st.header("Input Parameters")
weight = st.number_input("Body Weight (kg)", min_value=1.0, value=70.0, step=0.1)
height = st.number_input("Height (cm)", min_value=50.0, value=170.0, step=0.1)
bmi = weight / ((height / 100) ** 2)
st.write(f"Calculated BMI: {bmi:.2f}")

age = st.number_input("Age (years)", min_value=0, value=30, step=1)
sex = st.radio("Sex", options=["Male", "Female"])
sex_value = 1 if sex == "Male" else 0

# Optional: Jackson-Pollock method
st.header("Optional: Jackson-Pollock Method")
method = st.radio("Choose Method", options=["None", "3-Site", "7-Site"])

skinfold_inputs = {}
sum_skinfolds = 0

if method == "3-Site":
    st.write("Enter skinfold measurements for 3 sites:")
    if sex == "Male":
        skinfold_inputs["Chest"] = st.number_input("Chest Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)
        skinfold_inputs["Abdomen"] = st.number_input("Abdomen Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)
        skinfold_inputs["Thigh"] = st.number_input("Thigh Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)
    else:
        skinfold_inputs["Triceps"] = st.number_input("Triceps Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)
        skinfold_inputs["Suprailiac"] = st.number_input("Suprailiac Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)
        skinfold_inputs["Thigh"] = st.number_input("Thigh Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)
elif method == "7-Site":
    st.write("Enter skinfold measurements for 7 sites:")
    skinfold_inputs["Chest"] = st.number_input("Chest Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)
    skinfold_inputs["Midaxillary"] = st.number_input("Midaxillary Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)
    skinfold_inputs["Triceps"] = st.number_input("Triceps Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)
    skinfold_inputs["Subscapular"] = st.number_input("Subscapular Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)
    skinfold_inputs["Abdomen"] = st.number_input("Abdomen Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)
    skinfold_inputs["Suprailiac"] = st.number_input("Suprailiac Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)
    skinfold_inputs["Thigh"] = st.number_input("Thigh Skinfold (mm)", min_value=0.0, value=10.0, step=0.1)

# Calculate sum of skinfolds
if skinfold_inputs:
    sum_skinfolds = sum(skinfold_inputs.values())

# Optional: Density for Siri equation
density = st.number_input("Body Density (g/cm³)", min_value=0.0, value=1.05, step=0.01)

# Calculations
fat_mass = calculate_fat_mass(bmi, age, sex_value)
fat_free_mass = calculate_fat_free_mass(weight, fat_mass)
ffmi = calculate_ffmi(fat_free_mass, height / 100)
body_fat_percentage = calculate_body_fat_percentage(bmi, age, sex_value)

if method != "None" and sum_skinfolds > 0:
    if method == "3-Site":
        body_density = calculate_body_density_3_site(sex_value, sum_skinfolds, age)
    else:
        body_density = calculate_body_density_7_site(sex_value, sum_skinfolds, age)
    jackson_pollock_body_fat = calculate_body_fat_siri(body_density)
else:
    body_density = jackson_pollock_body_fat = None

if density > 0:
    siri_body_fat = calculate_body_fat_siri(density)
else:
    siri_body_fat = None

# Display results
st.header("Results")
results = {
    "Weight": f"{weight:.2f} kg",
    "Height": f"{height:.2f} cm",
    "BMI": f"{bmi:.2f}",
    "Fat Mass (FM)": f"{fat_mass:.2f} kg",
    "Fat-Free Mass (FFM)": f"{fat_free_mass:.2f} kg",
    "Fat-Free Mass Index (FFMI)": f"{ffmi:.2f}",
    "Body Fat Percentage (BMI Method)": f"{body_fat_percentage:.2f} %",
}

if density > 0:
    results["Body Fat Percentage (Siri Equation)"] = f"{siri_body_fat:.2f} %"

if method != "None" and sum_skinfolds > 0:
    results["Body Density (Jackson-Pollock)"] = f"{body_density:.4f} g/cm³"
    results["Body Fat Percentage (Jackson-Pollock)"] = f"{jackson_pollock_body_fat:.2f} %"
    results["Sum of Skinfolds"] = f"{sum_skinfolds:.2f} mm"

for site, thickness in skinfold_inputs.items():
    results[f"Skinfold Thickness ({site})"] = f"{thickness:.2f} mm"

for key, value in results.items():
    st.write(f"{key}: {value}")

# Formulas and References
st.header("Formulas")
formulas = [
    "Fat Mass (FM): (1.2 * BMI) + (0.23 * Age) - (10.8 * Sex) - 5.4",
    "Fat-Free Mass Index (FFMI): FFM / Height^2",
    "Body Fat Percentage (Siri Equation): (4.95 / Density - 4.50) * 100",
    "Body Density (3-Site): See Jackson-Pollock Equations"
]
for formula in formulas:
    st.write(formula)

st.header("References")
references = [
    "1. Deurenberg et al., 1991. BMI as a measure of fatness.",
    "2. Siri, W.E., 1956. Body composition from fluid spaces.",
    "3. Jackson & Pollock, 1978. Generalized equations for predicting body density."
]
for ref in references:
    st.write(ref)

# PDF Download
st.header("Download Results as PDF")
if st.button("Generate PDF"):
    pdf_buffer = create_pdf(results, formulas, references)
    st.download_button(
        label="Download PDF",
        data=pdf_buffer,
        file_name="body_composition_report.pdf",
        mime="application/pdf",
    )
