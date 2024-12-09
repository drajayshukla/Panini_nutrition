import streamlit as st
import pandas as pd
from fpdf import FPDF
import random
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

# Load the diet data
diet_data = pd.read_csv('data/our_diet11.csv')

# Ensure numeric columns
diet_data["Kcal"] = pd.to_numeric(diet_data["Kcal"], errors="coerce")
diet_data["Protein Content (g)"] = pd.to_numeric(diet_data["Protein Content (g)"], errors="coerce")

# Function to select food items for a meal type
def select_items(meal_type, mandatory_subtypes, optional_subtypes=None, prob_random=None, veg_only=False, calorie_distribution=None):
    items = []

    if calorie_distribution and calorie_distribution.get(meal_type, 0) == 0:
        return items  # Skip this meal type if its calorie allocation is 0

    for subtype in mandatory_subtypes:
        choices = diet_data[diet_data["subcode"] == subtype]
        if veg_only:
            choices = choices[choices["Veg/Non_Veg"] == "Veg"]
        if not choices.empty:
            items.append(choices.sample(1).to_dict('records')[0])

    if optional_subtypes and prob_random and random.random() < prob_random:
        random_subtype = random.choice(optional_subtypes)
        random_choice = diet_data[diet_data["subcode"] == random_subtype]
        if veg_only:
            random_choice = random_choice[random_choice["Veg/Non_Veg"] == "Veg"]
        if not random_choice.empty:
            items.append(random_choice.sample(1).to_dict('records')[0])

    return items

# Function to generate a daily diet chart
def generate_daily_chart(total_calories, calorie_distribution, veg_only):
    meal_structure = {
        "A": (["A1", "A2"], ["A3"], 0.3),
        "B": (["B1", "B2"], None, None),
        "C": (["C1", "C2", "C3", "C4"], None, None),
        "D": (["D1"], ["D3"], 0.1),
        "E": (["E1"], ["E3"], 0.5),
        "F": (["F1"], None, None)
    }

    daily_chart = []
    total_calories_calculated = 0
    total_protein_calculated = 0

    for meal_type, (mandatory_subtypes, optional_subtypes, prob_random) in meal_structure.items():
        if calorie_distribution.get(meal_type, 0) == 0:
            continue

        items = select_items(meal_type, mandatory_subtypes, optional_subtypes, prob_random, veg_only, calorie_distribution)
        for item in items:
            daily_chart.append(item)
            total_calories_calculated += item["Kcal"]
            total_protein_calculated += item["Protein Content (g)"]

    adjustment_factor = total_calories / total_calories_calculated if total_calories_calculated > 0 else 1

    for item in daily_chart:
        item["Kcal"] = round(item["Kcal"] * adjustment_factor, 2)
        item["Protein Content (g)"] = round(item["Protein Content (g)"] * adjustment_factor, 2)

    total_calories_adjusted = sum(item["Kcal"] for item in daily_chart)
    total_protein_adjusted = sum(item["Protein Content (g)"] for item in daily_chart)

    return daily_chart, total_calories_adjusted, total_protein_adjusted, adjustment_factor

# Generate the monthly diet chart
def generate_monthly_chart(total_calories, calorie_distribution, veg_only):
    monthly_chart = []
    for _ in range(7):  # Generate for 7 days
        daily_chart, daily_calories, daily_protein, factor = generate_daily_chart(total_calories, calorie_distribution, veg_only)
        monthly_chart.append({
            "daily_chart": daily_chart,
            "daily_calories": daily_calories,
            "daily_protein": daily_protein,
            "adjustment_factor": factor
        })
    return monthly_chart

# Custom Hindi PDF Class
class HindiPDF(FPDF):
    def __init__(self):
        super().__init__()
        # Resolve the font path dynamically
        font_path = Path(__file__).resolve().parent.parent / "NotoSansDevanagari-Regular.ttf"
        print(f"Resolved font path: {font_path}")

        if not font_path.exists():
            raise FileNotFoundError(f"{font_path} font file not found! Please ensure it is in the correct folder.")

        # Add the Noto Sans Devanagari font for use in PDF
        self.add_font("NotoSansDevanagari", style="", fname=str(font_path), uni=True)

# Create PDF with Hindi Support
def create_pdf(monthly_chart, file_path, total_calories, calorie_distribution, veg_only):
    # Initialize HindiPDF class
    pdf = HindiPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # First Page: User Inputs Summary
    pdf.add_page()
    pdf.set_font("NotoSansDevanagari", size=12)
    pdf.cell(0, 10, "मासिक आहार चार्ट - उपयोगकर्ता इनपुट", ln=True, align="C", border=0)

    pdf.set_font("NotoSansDevanagari", size=10)
    pdf.ln(5)  # Add a blank line
    pdf.cell(0, 10, f"कुल दैनिक कैलोरी आवश्यकता: {total_calories} kcal", ln=True, border=0)
    pdf.cell(0, 10, "कैलोरी वितरण:", ln=True, border=0)

    # List the calorie distribution for each meal
    for meal, calories in calorie_distribution.items():
        pdf.cell(0, 10, f"  - {meal}: {calories} kcal", ln=True, border=0)

    pdf.cell(0, 10, f"आहार वरीयता: {'शाकाहारी' if veg_only else 'मिश्रित'}", ln=True, border=0)

    # Daily Diet Charts
    for day, daily_data in enumerate(monthly_chart, start=1):
        pdf.add_page()
        pdf.set_font("NotoSansDevanagari", size=12)
        pdf.cell(0, 10, f"दिन {day}: आहार चार्ट", ln=True, border=0)

        # Add table headers
        pdf.set_font("NotoSansDevanagari", size=10)
        pdf.set_fill_color(230, 230, 250)  # Light lavender for table headers
        pdf.cell(70, 10, "भोजन का नाम", border=1, fill=True, align="C")
        pdf.cell(40, 10, "मात्रा", border=1, fill=True, align="C")
        pdf.cell(40, 10, "कैलोरी (kcal)", border=1, fill=True, align="C")
        pdf.cell(40, 10, "प्रोटीन (g)", border=1, fill=True, align="C")
        pdf.ln()

        # Loop through food items and add them
        for item in daily_data["daily_chart"]:
            # Wrap text in the first column using multi_cell
            y_before = pdf.get_y()  # Save the current y position
            pdf.multi_cell(70, 10, item["Name"], border=1, align="L")  # Wrap text for the "Name" column
            y_after = pdf.get_y()  # Get the new y position after wrapping

            # Align other cells with the height of the wrapped text
            row_height = y_after - y_before
            x, y = pdf.get_x() + 70, y_before  # Move x to the start of the next cell, keep y consistent
            pdf.set_xy(x, y)
            pdf.cell(40, row_height, item["Quantities"], border=1, align="L")
            pdf.cell(40, row_height, f"{item['Kcal']:.2f}", border=1, align="R")
            pdf.cell(40, row_height, f"{item['Protein Content (g)']:.2f}", border=1, align="R")
            pdf.ln(row_height)  # Move to the next line

    # Output the PDF to the specified file path
    pdf.output(file_path)
    return file_path



# Streamlit App
st.title("व्यक्तिगत मासिक आहार चार्ट जनरेटर")

total_calories = st.number_input("अपनी कुल दैनिक कैलोरी आवश्यकता दर्ज करें (kcal):", min_value=300, max_value=4000, step=50, value=2000)
calorie_distribution = {
    "A": st.number_input("नाश्ता (A):", min_value=0, value=500),
    "B": st.number_input("सुबह का नाश्ता (B):", min_value=0, value=200),
    "C": st.number_input("दोपहर का भोजन (C):", min_value=0, value=800),
    "D": st.number_input("शाम का नाश्ता (D):", min_value=0, value=200),
    "E": st.number_input("रात्रि भोजन (E):", min_value=0, value=300),
    "F": st.number_input("सोते समय का नाश्ता (F):", min_value=0, value=0),
}
veg_only = st.radio("क्या आप केवल शाकाहारी आहार चाहते हैं?", options=[True, False], format_func=lambda x: "हां" if x else "नहीं")

if st.button("आहार चार्ट उत्पन्न करें"):
    monthly_chart = generate_monthly_chart(total_calories, calorie_distribution, veg_only)

    output_pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    create_pdf(monthly_chart, output_pdf_path, total_calories, calorie_distribution, veg_only)

    with open(output_pdf_path, "rb") as pdf_file:
        st.download_button("आहार चार्ट PDF डाउनलोड करें", pdf_file, "monthly_diet_chart.pdf")
