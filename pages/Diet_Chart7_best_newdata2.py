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

    # Skip this meal type if its calorie allocation is 0
    if calorie_distribution and calorie_distribution.get(meal_type, 0) == 0:
        return items  # Return an empty list

    # Select one item from each mandatory subtype
    for subtype in mandatory_subtypes:
        choices = diet_data[diet_data["subcode"] == subtype]
        if veg_only:
            choices = choices[choices["Veg/Non_Veg"] == "Veg"]
        if not choices.empty:
            items.append(choices.sample(1).to_dict('records')[0])

    # Optionally select one item from optional subtypes based on probability
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
        "A": (["A1", "A2"], ["A3"], 0.3),  # Breakfast
        "B": (["B1", "B2"], None, None),   # Morning Snack
        "C": (["C1", "C2", "C3", "C4"], None, None),  # Lunch
        "D": (["D1"], ["D3"], 0.1),  # Evening Snack
        "E": (["E1"], ["E3"], 0.5),  # Dinner
        "F": (["F1"], None, None)         # Bedtime Snack
    }

    daily_chart = []
    total_calories_calculated = 0
    total_protein_calculated = 0

    for meal_type, (mandatory_subtypes, optional_subtypes, prob_random) in meal_structure.items():
        if calorie_distribution.get(meal_type, 0) == 0:
            continue

        items = select_items(
            meal_type,
            mandatory_subtypes,
            optional_subtypes,
            prob_random,
            veg_only,
            calorie_distribution
        )
        for item in items:
            daily_chart.append(item)
            total_calories_calculated += item["Kcal"]
            total_protein_calculated += item["Protein Content (g)"]

    # Calculate adjustment factor
    adjustment_factor = total_calories / total_calories_calculated if total_calories_calculated > 0 else 1

    # Scale items based on adjustment factor
    for item in daily_chart:
        item["Kcal"] = round(item["Kcal"] * adjustment_factor, 2)
        item["Protein Content (g)"] = round(item["Protein Content (g)"] * adjustment_factor, 2)

    # Recalculate total calories and protein after adjustment
    total_calories_adjusted = sum(item["Kcal"] for item in daily_chart)
    total_protein_adjusted = sum(item["Protein Content (g)"] for item in daily_chart)

    return daily_chart, total_calories_adjusted, total_protein_adjusted, adjustment_factor


# Generate the monthly diet chart
def generate_monthly_chart(total_calories, calorie_distribution, veg_only):
    monthly_chart = []
    for _ in range(2):  # For 7 days (can be extended)
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
        font_path = Path("DejaVuSans.ttf")
        if not font_path.exists():
            raise FileNotFoundError("DejaVuSans.ttf font file not found!")
        self.add_font("DejaVu", style="", fname="DejaVuSans.ttf", uni=True)

    def add_wrapped_cell(self, width, height, text, border=1, align="L", fill=False):
        x, y = self.get_x(), self.get_y()
        self.multi_cell(width, height, text, border=border, align=align, fill=fill)
        self.set_xy(x + width, y)


# Create PDF with Hindi Support
def create_pdf(monthly_chart, file_path, total_calories, calorie_distribution, veg_only):
    pdf = HindiPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add First Page: User Inputs
    pdf.add_page()
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 10, "मासिक आहार चार्ट - उपयोगकर्ता इनपुट", ln=True, align="C")
    pdf.set_font("DejaVu", size=10)
    pdf.cell(0, 10, f"कुल दैनिक कैलोरी आवश्यकता: {total_calories} kcal", ln=True)
    pdf.cell(0, 10, "कैलोरी वितरण:", ln=True)
    for meal, calories in calorie_distribution.items():
        pdf.cell(0, 10, f"  - {meal}: {calories} kcal", ln=True)
    pdf.cell(0, 10, f"आहार वरीयता: {'शाकाहारी' if veg_only else 'मिश्रित'}", ln=True)

    # Add daily diet charts
    for day, daily_data in enumerate(monthly_chart, start=1):
        pdf.add_page()
        pdf.set_font("DejaVu", size=12)
        pdf.cell(0, 10, f"दिन {day}: आहार चार्ट", ln=True)
        pdf.set_font("DejaVu", size=10)
        for item in daily_data["daily_chart"]:
            pdf.add_wrapped_cell(70, 8, item["Name"], border=1)
            pdf.cell(40, 8, item["Quantities"], border=1, align="L")
            pdf.cell(40, 8, f"{item['Kcal']:.2f}", border=1, align="R")
            pdf.cell(40, 8, f"{item['Protein Content (g)']:.2f}", border=1, align="R")
            pdf.ln()

    pdf.output(file_path)
    return file_path


# Streamlit App
st.title("व्यक्तिगत मासिक आहार चार्ट जनरेटर")

# Inputs
total_calories = st.number_input("अपनी कुल दैनिक कैलोरी आवश्यकता दर्ज करें (kcal):", min_value=300, max_value=4000, step=50, value=2000)
st.write("अपने भोजन के लिए कैलोरी वितरित करें:")
calorie_distribution = {
    "A": st.number_input("नाश्ता (A) (kcal):", min_value=0, max_value=total_calories, step=50, value=500),
    "B": st.number_input("सुबह का नाश्ता (B) (kcal):", min_value=0, max_value=total_calories, step=50, value=200),
    "C": st.number_input("दोपहर का भोजन (C) (kcal):", min_value=0, max_value=total_calories, step=50, value=800),
    "D": st.number_input("शाम का नाश्ता (D) (kcal):", min_value=0, max_value=total_calories, step=50, value=200),
    "E": st.number_input("रात्रि भोजन (E) (kcal):", min_value=0, max_value=total_calories, step=50, value=300),
    "F": st.number_input("सोते समय का नाश्ता (F) (kcal):", min_value=0, max_value=total_calories, step=50, value=0),
}

veg_only = st.radio("क्या आप केवल शाकाहारी आहार चाहते हैं?", options=[True, False], format_func=lambda x: "हां" if x else "नहीं")

if st.button("आहार चार्ट उत्पन्न करें"):
    monthly_chart = generate_monthly_chart(total_calories, calorie_distribution, veg_only)

    # Create and download PDF
    output_pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    create_pdf(monthly_chart, output_pdf_path, total_calories, calorie_distribution, veg_only)

    with open(output_pdf_path, "rb") as pdf_file:
        st.download_button("आहार चार्ट PDF डाउनलोड करें", pdf_file, "monthly_diet_chart.pdf")
