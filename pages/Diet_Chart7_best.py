import streamlit as st
import pandas as pd
from fpdf import FPDF
import random
import tempfile


# Load the diet data
diet_data = pd.read_csv('data/mydiet.csv')

# Ensure numeric columns
diet_data["Kcal"] = pd.to_numeric(diet_data["Kcal"], errors="coerce")
diet_data["Protein Content (g)"] = pd.to_numeric(diet_data["Protein Content (g)"], errors="coerce")

# Function to select food items for a meal type based on subtypes and preferences
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
        "D": (["D1", "D2"], ["D3"], 0.1),  # Evening Snack
        "E": (["E1", "E2", "E3"], ["E4", "E5"], 0.5),  # Dinner
        "F": (["F1"], None, None)         # Bedtime Snack
    }

    daily_chart = []
    total_calories_calculated = 0
    total_protein_calculated = 0

    for meal_type, (mandatory_subtypes, optional_subtypes, prob_random) in meal_structure.items():
        items = select_items(meal_type, mandatory_subtypes, optional_subtypes, prob_random, veg_only, calorie_distribution)
        for item in items:
            daily_chart.append(item)
            total_calories_calculated += item["Kcal"]
            total_protein_calculated += item["Protein Content (g)"]

    # Calculate adjustment factor if needed
    adjustment_factor = total_calories / total_calories_calculated if total_calories_calculated > 0 else 1
    return daily_chart, total_calories_calculated, total_protein_calculated, adjustment_factor


# Generate the monthly diet chart
def generate_monthly_chart(total_calories, calorie_distribution, veg_only):
    monthly_chart = []
    for _ in range(7):  # 30 days in a month
        daily_chart, daily_calories, daily_protein, factor = generate_daily_chart(total_calories, calorie_distribution, veg_only)
        monthly_chart.append({
            "daily_chart": daily_chart,
            "daily_calories": daily_calories,
            "daily_protein": daily_protein,
            "adjustment_factor": factor
        })
    return monthly_chart

# Create a PDF with the monthly chart
from fpdf import FPDF

from fpdf import FPDF



def create_pdf(monthly_chart, file_path, total_calories, calorie_distribution, veg_only):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    def add_wrapped_cell(pdf, width, height, text, border=1, align='L', fill=False):
        """
        Adds a wrapped cell using MultiCell if the text is too long.
        """
        x, y = pdf.get_x(), pdf.get_y()
        pdf.multi_cell(width, height, text, border=border, align=align, fill=fill)
        pdf.set_xy(x + width, y)  # Reset cursor to the right of the cell

    # Add First Page: User Inputs
    pdf.add_page()
    pdf.set_font("Arial", size=10, style="B")
    pdf.set_fill_color(173, 216, 230)  # Light blue
    pdf.cell(0, 10, "Monthly Diet Chart - User Inputs", ln=True, align='C', fill=True)
    pdf.set_font("Arial", size=10)
    pdf.ln(10)
    pdf.cell(0, 10, f"Total Daily Calorie Requirement: {total_calories} kcal", ln=True)
    pdf.cell(0, 10, "Calorie Distribution:", ln=True)
    for meal, calories in calorie_distribution.items():
        pdf.cell(0, 10, f"  - {meal}: {calories} kcal", ln=True)
    pdf.cell(0, 10, f"Diet Preference: {'Vegetarian' if veg_only else 'Mixed (Veg + Non-Veg)'}", ln=True)

    # Add a blank line
    # Add a blank line
    pdf.ln(5)

    # Add summary for daily calorie surplus or deficit and multiplication factor
    pdf.set_font("Arial", size=10, style="B")
    pdf.cell(0, 10, "Daily Calorie Surplus or Deficit and Multiplication Factor:", ln=True)
    pdf.set_font("Arial", size=10)
    for day, daily_data in enumerate(monthly_chart, start=1):
        surplus_deficit = calculate_calorie_surplus_deficit(daily_data["daily_calories"], total_calories)
        multiplication_factor = total_calories / daily_data["daily_calories"] if daily_data["daily_calories"] > 0 else 1
        if surplus_deficit > 0:
            pdf.cell(0, 10,
                     f"Day {day}: Surplus of {surplus_deficit:.2f} kcal, Multiplication Factor: {multiplication_factor:.2f}",
                     ln=True)
        elif surplus_deficit < 0:
            pdf.cell(0, 10,
                     f"Day {day}: Deficit of {abs(surplus_deficit):.2f} kcal, Multiplication Factor: {multiplication_factor:.2f}",
                     ln=True)
        else:
            pdf.cell(0, 10,
                     f"Day {day}: Balanced at {total_calories} kcal, Multiplication Factor: {multiplication_factor:.2f}",
                     ln=True)



    # Individual daily charts
    for day, daily_data in enumerate(monthly_chart, start=1):
        pdf.add_page()
        pdf.set_font("Arial", size=10, style="B")
        pdf.set_fill_color(144, 238, 144)  # Light green

        from datetime import datetime, timedelta
        start_date = datetime.now()
        current_date = start_date + timedelta(days=day - 1)
        pdf.cell(0, 10, f"{current_date.strftime('%A, %d %B %Y')} - Diet Chart", ln=True, fill=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, f"Daily Calories: {daily_data['daily_calories']:.2f} kcal", ln=True)
        pdf.cell(0, 10, f"Daily Protein: {daily_data['daily_protein']:.2f} g", ln=True)

        # Calculate and include multiplication factor
        multiplication_factor = total_calories / daily_data["daily_calories"] if daily_data["daily_calories"] > 0 else 1
        pdf.cell(0, 10, f"Multiplication Factor: {multiplication_factor:.2f}", ln=True)

        surplus_deficit = calculate_calorie_surplus_deficit(daily_data["daily_calories"], total_calories)
        if surplus_deficit > 0:
            pdf.set_text_color(0, 128, 0)  # Green for surplus
            pdf.cell(0, 10, f"Calorie Surplus: {surplus_deficit:.2f} kcal", ln=True)
        elif surplus_deficit < 0:
            pdf.set_text_color(255, 0, 0)  # Red for deficit
            pdf.cell(0, 10, f"Calorie Deficit: {abs(surplus_deficit):.2f} kcal", ln=True)
        else:
            pdf.set_text_color(0, 0, 0)  # Black for balanced
            pdf.cell(0, 10, f"Calories Balanced at {total_calories} kcal", ln=True)
        pdf.set_text_color(0, 0, 0)

        # Section headers and grouped items
        sections = {
            "Breakfast": ["A1", "A2", "A3"],
            "Morning Snacks": ["B1", "B2"],
            "Lunch": ["C1", "C2", "C3", "C4"],
            "Evening Snacks": ["D1", "D2", "D3"],
            "Dinner": ["E1", "E2", "E3", "E4", "E5"],
            "Bedtime": ["F1"]
        }

        # Dynamically adjust column widths
        col_widths = [70, 40, 40, 40]
        row_height = 8  # Dynamic row height to ensure no overlap

        for section, subcodes in sections.items():
            # Check if there's enough space for the section header and rows
            if pdf.get_y() > 260:  # Adjust threshold based on page height
                pdf.add_page()

            pdf.set_font("Arial", size=12, style="B")
            pdf.set_fill_color(255, 222, 173)  # Light orange
            pdf.cell(0, 10, section, ln=True, fill=True)
            pdf.set_font("Arial", size=10)
            pdf.set_fill_color(230, 230, 250)  # Light lavender for table headers
            pdf.cell(col_widths[0], row_height, "Food Item", border=1, fill=True, align='C')
            pdf.cell(col_widths[1], row_height, "Quantity", border=1, fill=True, align='C')
            pdf.cell(col_widths[2], row_height, "Calories (kcal)", border=1, fill=True, align='C')
            pdf.cell(col_widths[3], row_height, "Protein (g)", border=1, fill=True, align='C')
            pdf.ln()

            # Add items for the section
            for item in daily_data["daily_chart"]:
                if item["subcode"] in subcodes:
                    add_wrapped_cell(pdf, col_widths[0], row_height, item["Name"], border=1, align='L')
                    pdf.cell(col_widths[1], row_height, item["Quantities"], border=1, align='L')
                    pdf.cell(col_widths[2], row_height, f"{item['Kcal']:.2f}", border=1, align='R')
                    pdf.cell(col_widths[3], row_height, f"{item['Protein Content (g)']:.2f}", border=1, align='R')
                    pdf.ln()

    pdf.output(file_path)
    return file_path






# Calculate calorie surplus or deficit
def calculate_calorie_surplus_deficit(daily_calories, total_calories):
    return daily_calories - total_calories

# Streamlit app
st.title("Personalized Monthly Diet Chart Generator")

# Input for total calories
total_calories = st.number_input("Enter your total daily calorie requirement (kcal):", min_value=300, max_value=4000, step=50, value=1000)

# Input for calorie distribution
st.write("Distribute your calories across meals (A to F).")
calorie_distribution = {
    "A": st.number_input("Breakfast (A) (kcal):", min_value=0, max_value=total_calories, step=50, value=200),
    "B": st.number_input("Morning Snack (B) (kcal):", min_value=0, max_value=total_calories, step=50, value=0),
    "C": st.number_input("Lunch (C) (kcal):", min_value=0, max_value=total_calories, step=50, value=300),
    "D": st.number_input("Evening Snack (D) (kcal):", min_value=0, max_value=total_calories, step=50, value=100),
    "E": st.number_input("Dinner (E) (kcal):", min_value=0, max_value=total_calories, step=50, value=200),
    "F": st.number_input("Bedtime Snack (F) (kcal):", min_value=0, max_value=total_calories, step=50, value=0),
}

# Veg-only option
veg_only = st.radio("Do you want a vegetarian-only diet?", options=[True, False], format_func=lambda x: "Yes" if x else "No")

# Validate calorie distribution
if sum(calorie_distribution.values()) > total_calories:
    st.error("The total calorie distribution exceeds the daily calorie requirement. Please adjust your inputs.")
else:
    if st.button("Generate Diet Chart"):
        monthly_chart = generate_monthly_chart(total_calories, calorie_distribution, veg_only)
        output_pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
        create_pdf(monthly_chart, output_pdf_path, total_calories, calorie_distribution, veg_only)

        st.subheader("Daily Calorie Surplus or Deficit")
        for day, daily_data in enumerate(monthly_chart, start=1):
            surplus_deficit = calculate_calorie_surplus_deficit(daily_data['daily_calories'], total_calories)
            if surplus_deficit > 0:
                st.write(f"Day {day}: Surplus of {surplus_deficit:.2f} kcal")
            elif surplus_deficit < 0:
                st.write(f"Day {day}: Deficit of {abs(surplus_deficit):.2f} kcal")
            else:
                st.write(f"Day {day}: Balanced at {total_calories} kcal")

        st.success("Diet chart generated successfully!")
        with open(output_pdf_path, "rb") as pdf_file:
            st.download_button("Download Diet Chart PDF", pdf_file, "monthly_diet_chart1.pdf")

