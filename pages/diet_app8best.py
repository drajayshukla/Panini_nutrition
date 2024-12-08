import streamlit as st
import json
import random
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
import os

# Load diet JSON data
json_path = "data/dietdrajaybest.json"
with open(json_path, "r") as file:
    diet_data = json.load(file)


# Function to calculate total calories for a meal
def calculate_calories(meal):
    return sum(float(item["Kcal"]) for item in meal)


# Adjust quantities using a multiplication factor
def adjust_quantities(meal, factor):
    adjusted_meal = []
    for item in meal:
        adjusted_item = item.copy()
        adjusted_item["Quantities"] = f"{factor:.2f} x {item['Quantities']}"
        adjusted_item["Kcal"] = float(item["Kcal"]) * factor
        adjusted_meal.append(adjusted_item)
    return adjusted_meal


# Generate diet plan with structured meals and calorie adjustments
def generate_diet_plan(total_kcal, meal_calories):
    """Generate a 30-day diet plan with structured meals."""
    daily_diet_plan = []

    for day in range(1, 31):
        daily_plan = {"Day": day}

        # Generate meals
        meals = {
            "Breakfast": [
                random.choice(diet_data["A1"]),
                random.choice(diet_data["A2"]),
                random.choice(diet_data["A3"]) if random.random() < 0.3 else None
            ],
            "Morning Snack": [
                random.choice(diet_data["B1"]),
                random.choice(diet_data["B2"])
            ],
            "Lunch": [
                random.choice(diet_data[sub]) for sub in ["C1", "C2", "C3", "C4"]
            ],
            "Evening Snack": [
                random.choice(diet_data["D1"]),
                random.choice(diet_data["D2"]),
                random.choice(diet_data["D3"]) if random.random() < 0.1 else None
            ],
            "Dinner": [
                          random.choice(diet_data[sub]) for sub in ["E1", "E2", "E3"]
                      ] + ([random.choice(diet_data["E4"]),
                            random.choice(diet_data["E5"])] if random.random() < 0.5 else []),
            "Bedtime": [
                random.choice(diet_data["F1"])
            ]
        }

        # Filter out `None` items and adjust meal calories
        for meal, target_calories in meal_calories.items():
            meals[meal] = [item for item in meals[meal] if item]  # Remove None items
            current_calories = calculate_calories(meals[meal])
            if current_calories > target_calories * 1.15:
                # Reduce quantities to fit within the range
                factor = target_calories * 1.15 / current_calories
                meals[meal] = adjust_quantities(meals[meal], factor)

        # Assign meals to the daily plan
        daily_plan.update(meals)

        # Calculate final total calories for the day
        total_calories_given = sum(calculate_calories(meals[meal]) for meal in meals)
        daily_plan["Total Calories Given"] = total_calories_given
        daily_plan["Total Calories Recommended"] = total_kcal

        daily_diet_plan.append(daily_plan)

    return daily_diet_plan


# Create PDF from the generated diet plan
def create_pdf(diet_plan, file_name="diet_plan.pdf"):
    """Create a PDF from the diet plan with one day per page."""
    pdf = SimpleDocTemplate(file_name, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    for day_plan in diet_plan:
        elements.append(Paragraph(f"Day {day_plan['Day']}", styles["Heading2"]))

        # Display structured meals
        for meal, items in day_plan.items():
            if meal not in ["Day", "Total Calories Given", "Total Calories Recommended"]:
                elements.append(Paragraph(f"{meal}:", styles["Heading3"]))
                data = [["Food", "Quantity", "Calories"]]
                for item in items:
                    data.append([item["Name"], item["Quantities"], f"{float(item['Kcal']):.2f}"])

                # Create table for the meal
                table = Table(data, colWidths=[200, 100, 100])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 12))  # Add spacing between meals

        # Add total calories for the day
        elements.append(
            Paragraph(f"Total Calories Recommended: {day_plan['Total Calories Recommended']:.2f}", styles["BodyText"]))
        elements.append(Paragraph(f"Total Calories Given: {day_plan['Total Calories Given']:.2f}", styles["BodyText"]))

        # Page break
        elements.append(PageBreak())

    pdf.build(elements)
    return file_name


# Streamlit app layout
st.title("Personalized Diet Plan Generator")
st.header("Generate a 30-Day Structured Diet Plan")

# User input for total calories
total_kcal = st.number_input("Enter your total daily calorie goal (kcal):", min_value=500, max_value=5000, step=100)

# Calorie allocation sliders with dynamic adjustment
st.subheader("Allocate Calories for Each Meal")
remaining_calories = total_kcal
meal_calories = {}

meal_calories["Breakfast"] = st.slider("Breakfast Calories:", min_value=0, max_value=remaining_calories,
                                       value=min(int(total_kcal * 0.25), remaining_calories))
remaining_calories -= meal_calories["Breakfast"]

meal_calories["Morning Snack"] = st.slider("Morning Snack Calories:", min_value=0, max_value=remaining_calories,
                                           value=min(int(total_kcal * 0.10), remaining_calories))
remaining_calories -= meal_calories["Morning Snack"]

meal_calories["Lunch"] = st.slider("Lunch Calories:", min_value=0, max_value=remaining_calories,
                                   value=min(int(total_kcal * 0.30), remaining_calories))
remaining_calories -= meal_calories["Lunch"]

meal_calories["Evening Snack"] = st.slider("Evening Snack Calories:", min_value=0, max_value=remaining_calories,
                                           value=min(int(total_kcal * 0.10), remaining_calories))
remaining_calories -= meal_calories["Evening Snack"]

meal_calories["Dinner"] = st.slider("Dinner Calories:", min_value=0, max_value=remaining_calories,
                                    value=min(int(total_kcal * 0.20), remaining_calories))
remaining_calories -= meal_calories["Dinner"]

meal_calories["Bedtime"] = st.slider("Bedtime Calories:", min_value=0, max_value=remaining_calories,
                                     value=remaining_calories)

# Generate the diet plan and PDF
if st.button("Generate Diet Plan"):
    if total_kcal > 0:
        diet_plan = generate_diet_plan(total_kcal, meal_calories)
        pdf_file = create_pdf(diet_plan)
        with open(pdf_file, "rb") as pdf:
            st.download_button(
                label="Download Diet Plan as PDF",
                data=pdf,
                file_name="diet_plan.pdf",
                mime="application/pdf",
            )
        os.remove(pdf_file)
    else:
        st.error("Please enter a valid calorie goal.")
