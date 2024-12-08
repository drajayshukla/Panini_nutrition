import streamlit as st

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

# Signs and symptoms
st.subheader("Signs and Symptoms")
with st.expander("General Appearance"):
    central_obesity = st.checkbox("Central Obesity")
    dysmorphic_features = st.checkbox("Dysmorphic Features (e.g., wide-set eyes, low-set ears)")
    acanthosis_nigricans = st.checkbox("Acanthosis Nigricans")
    skin_tags = st.checkbox("Skin Tags")
    striae = st.checkbox("Striae")
    hyperpigmentation = st.checkbox("Hyperpigmentation")

with st.expander("Neurological"):
    developmental_delay = st.checkbox("Developmental Delay")
    seizures = st.checkbox("Seizures")
    hypotonia = st.checkbox("Hypotonia")
    hyperactivity = st.checkbox("Hyperactivity or Inattention")

with st.expander("Endocrine Signs"):
    precocious_puberty = st.checkbox("Precocious Puberty")
    growth_abnormalities = st.checkbox("Growth Velocity Abnormalities")
    hypothyroid_symptoms = st.checkbox("Signs of Hypothyroidism (cold intolerance, lethargy)")

with st.expander("Cardiorespiratory"):
    sleep_apnea = st.checkbox("Sleep Apnea")
    hypertension = st.checkbox("Hypertension")
    tachycardia = st.checkbox("Tachycardia")
    dyspnea = st.checkbox("Dyspnea on Exertion")

with st.expander("Musculoskeletal"):
    bowing_of_legs = st.checkbox("Bowing of Legs")
    joint_pain = st.checkbox("Joint Pain")

with st.expander("Psychosocial"):
    behavioral_issues = st.checkbox("Behavioral Issues")
    poor_academic = st.checkbox("Poor Academic Performance")

# Investigations
st.header("Investigations")

st.subheader("Routine Laboratory Investigations")
cbc = st.checkbox("Complete Blood Count (CBC)")
fbglucose = st.checkbox("Fasting Blood Glucose (FBG)")
lipid_profile = st.checkbox("Lipid Profile")
lfts = st.checkbox("Liver Function Tests (LFTs)")
rfts = st.checkbox("Renal Function Tests (RFTs)")

st.subheader("Endocrine Assessment")
tfts = st.checkbox("Thyroid Function Tests (TFTs)")
insulin_cpeptide = st.checkbox("Fasting Insulin and C-Peptide")
cortisol = st.checkbox("Cortisol (Morning)")
gh_igf1 = st.checkbox("Growth Hormone (GH) / IGF-1")
adrenal_tests = st.checkbox("Adrenal Function Tests (ACTH, DHEA-S)")

st.subheader("Genetic Investigations")
genetic_tests = st.multiselect(
    "Genetic Testing",
    [
        "Leptin (LEP) and Leptin Receptor (LEPR) Mutation",
        "Pro-opiomelanocortin (POMC) Mutation",
        "Melanocortin 4 Receptor (MC4R) Mutation",
        "Prader-Willi Syndrome (PWS) Methylation Analysis",
        "Bardet-Biedl Syndrome (BBS) Gene Testing"
    ]
)

st.subheader("Metabolic Screening")
electrolytes = st.checkbox("Serum Electrolytes (Na+, K+, Ca²+)")
uric_acid = st.checkbox("Serum Uric Acid")
vitamin_levels = st.checkbox("Serum Vitamin D and B12")
plasma_amino = st.checkbox("Plasma Amino Acids")

st.subheader("Imaging Studies")
imaging = st.multiselect(
    "Imaging",
    ["Abdominal Ultrasound", "Echocardiography", "MRI Brain"]
)

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
        "Signs of endocrinopathy (precocious puberty, short stature, hypothyroidism)",
        "Family history of genetic or syndromic disorders"
    ]
)

# Summary and plan
st.header("Summary and Plan")
if st.button("Generate Report"):
    st.subheader("Patient Summary")
    st.write(f"**Name:** {name}")
    st.write(f"**Age:** {age} years")
    st.write(f"**Gender:** {gender}")
    st.write(f"**Weight:** {weight} kg")
    st.write(f"**Height:** {height} cm")
    st.write(f"**BMI:** {bmi} kg/m²")
    st.write(f"**Head Circumference:** {head_circumference} cm")

    st.subheader("Red Flag Signs Identified")
    st.write(", ".join(red_flags) if red_flags else "None")

    st.subheader("Investigations Ordered")
    investigations = []
    if cbc: investigations.append("Complete Blood Count (CBC)")
    if fbglucose: investigations.append("Fasting Blood Glucose (FBG)")
    if lipid_profile: investigations.append("Lipid Profile")
    if lfts: investigations.append("Liver Function Tests (LFTs)")
    if rfts: investigations.append("Renal Function Tests (RFTs)")
    if tfts: investigations.append("Thyroid Function Tests (TFTs)")
    if insulin_cpeptide: investigations.append("Fasting Insulin and C-Peptide")
    if cortisol: investigations.append("Cortisol (Morning)")
    if gh_igf1: investigations.append("Growth Hormone (GH) / IGF-1")
    if adrenal_tests: investigations.append("Adrenal Function Tests")
    investigations.extend(genetic_tests)
    if electrolytes: investigations.append("Serum Electrolytes")
    if uric_acid: investigations.append("Serum Uric Acid")
    if vitamin_levels: investigations.append("Serum Vitamin D and B12")
    if plasma_amino: investigations.append("Plasma Amino Acids")
    investigations.extend(imaging)
    st.write(", ".join(investigations) if investigations else "None")

    st.subheader("Plan of Management")
    st.write("- Lifestyle interventions: Diet and physical activity counseling")
    st.write("- Medical interventions: Based on underlying cause")
    st.write("- Referral to specialist if needed")
