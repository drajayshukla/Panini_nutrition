import streamlit as st
import pandas as pd
from fpdf import FPDF
import random
import tempfile
from datetime import datetime, timedelta


# Load the diet data
diet_data = pd.read_csv('data/our_diet.csv')

# Ensure numeric columns
diet_data["Kcal"] = pd.to_numeric(diet_data["Kcal"], errors="coerce")
diet_data["Protein Content (g)"] = pd.to_numeric(diet_data["Protein Content (g)"], errors="coerce")


# Function to select food items for a meal type based on subtypes and preferences
def select_items(meal_type, mandatory_subtypes, optional_subtypes=None, prob_random=None, veg_only=False, calorie_distribution=None):
    items = []
    if calorie_distribution and calorie_distribution.get(meal_type, 0) == 0:
        return items

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

    adjustment_factor = total_calories / total_calories_calculated if total_calories_calculated > 0 else 1

    for item in daily_chart:
        item["Kcal"] = round(item["Kcal"] * adjustment_factor, 2)
        item["Protein Content (g)"] = round(item["Protein Content (g)"] * adjustment_factor, 2)

    total_calories_adjusted = sum(item["Kcal"] for item in daily_chart)
    total_protein_adjusted = sum(item["Protein Content (g)"] for item in daily_chart)

    return daily_chart, total_calories_adjusted, total_protein_adjusted, adjustment_factor


# Generate the diet chart for a specified number of days
def generate_chart(total_calories, calorie_distribution, veg_only, num_days):
    chart = []
    for _ in range(num_days):
        daily_chart, daily_calories, daily_protein, factor = generate_daily_chart(total_calories, calorie_distribution, veg_only)
        chart.append({
            "daily_chart": daily_chart,
            "daily_calories": daily_calories,
            "daily_protein": daily_protein,
            "adjustment_factor": factor
        })
    return chart


# Create a PDF with the diet chart
def create_pdf(chart, file_path, total_calories, calorie_distribution, veg_only, num_days):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add user inputs page
    pdf.add_page()
    pdf.set_font("Arial", size=10, style="B")
    pdf.cell(0, 10, f"Diet Chart for {num_days} Days", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Total Daily Calorie Requirement: {total_calories} kcal", ln=True)
    pdf.cell(0, 10, f"Diet Preference: {'Vegetarian' if veg_only else 'Mixed (Veg + Non-Veg)'}", ln=True)

    # Add each day's chart
    for day, daily_data in enumerate(chart, start=1):
        pdf.add_page()
        pdf.set_font("Arial", size=10, style="B")
        current_date = (datetime.now() + timedelta(days=day - 1)).strftime('%A, %d %B %Y')
        pdf.cell(0, 10, f"{current_date} - Diet Chart", ln=True)

        # Add chart content
        for item in daily_data["daily_chart"]:
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 10, f"{item['Name']} - {item['Kcal']} kcal - {item['Protein Content (g)']} g", ln=True)

    pdf.output(file_path)
    return file_path


# Streamlit app
st.title("Personalized Diet Chart Generator")

# User inputs
total_calories = st.number_input("Enter your total daily calorie requirement (kcal):", min_value=300, max_value=4000, step=50, value=2000)
veg_only = st.radio("Do you prefer a vegetarian diet?", [True, False], format_func=lambda x: "Yes" if x else "No")
num_days = st.number_input("Number of days for the diet chart:", min_value=1, max_value=31, step=1, value=7)

calorie_distribution = {
    "A": st.number_input("Breakfast (kcal):", min_value=0, max_value=total_calories, step=50, value=500),
    "B": st.number_input("Morning Snack (kcal):", min_value=0, max_value=total_calories, step=50, value=200),
    "C": st.number_input("Lunch (kcal):", min_value=0, max_value=total_calories, step=50, value=600),
    "D": st.number_input("Evening Snack (kcal):", min_value=0, max_value=total_calories, step=50, value=200),
    "E": st.number_input("Dinner (kcal):", min_value=0, max_value=total_calories, step=50, value=500),
    "F": st.number_input("Bedtime Snack (kcal):", min_value=0, max_value=total_calories, step=50, value=100),
}

if st.button("Generate Diet Chart"):
    diet_chart = generate_chart(total_calories, calorie_distribution, veg_only, num_days)
    pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    create_pdf(diet_chart, pdf_path, total_calories, calorie_distribution, veg_only, num_days)

    with open(pdf_path, "rb") as f:
        st.download_button("Download Diet Chart PDF", f, "diet_chart.pdf")
