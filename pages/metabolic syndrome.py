import streamlit as st

def check_metabolic_syndrome(criteria):
    return sum(criteria) >= 3

st.title("Metabolic Syndrome Evaluation")

st.write("### Enter your measurements and conditions:")

# Input fields
gender = st.radio("Gender", ["Female", "Male"])
waist_circumference = st.number_input("Waist Circumference (cm):", min_value=0.0, step=0.1)
triglycerides = st.number_input("Triglycerides (mmol/L):", min_value=0.0, step=0.1)
hdl_cholesterol = st.number_input("HDL Cholesterol (mmol/L):", min_value=0.0, step=0.1)
systolic_bp = st.number_input("Systolic Blood Pressure (mmHg):", min_value=0, step=1)
diastolic_bp = st.number_input("Diastolic Blood Pressure (mmHg):", min_value=0, step=1)
fasting_glucose = st.number_input("Fasting Glucose (mmol/L):", min_value=0.0, step=0.1)

# Checkbox for medication or history
med_tg = st.checkbox("On medication for elevated triglycerides?")
med_hdl = st.checkbox("On medication for reduced HDL?")
med_bp = st.checkbox("On medication for hypertension?")
med_glucose = st.checkbox("On medication for hyperglycemia?")

# Criteria evaluation
criteria = [
    waist_circumference >= 80 if gender == "Female" else waist_circumference >= 94,
    triglycerides >= 1.7 or med_tg,
    hdl_cholesterol < 1.0 if gender == "Male" else hdl_cholesterol < 1.3 or med_hdl,
    systolic_bp >= 130 or diastolic_bp >= 85 or med_bp,
    fasting_glucose >= 5.5 or med_glucose
]

# Diagnosis
if st.button("Evaluate"):
    if check_metabolic_syndrome(criteria):
        st.success("You meet the criteria for Metabolic Syndrome.")
    else:
        st.info("You do not meet the criteria for Metabolic Syndrome.")