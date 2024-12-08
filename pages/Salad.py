import streamlit as st
import pandas as pd
import random
from fpdf import FPDF
import tempfile


# Load the CSV file
def load_data():
    data = pd.read_csv("data/salads.csv")
    return data

# Generate random salads for morning and evening
def get_random_salads(data):
    morning_salad = data.sample(1).iloc[0]
    evening_salad = data.sample(1).iloc[0]
    return morning_salad, evening_salad

# Calculate daily calorie surplus/deficit
def calculate_surplus_deficit(calories, morning_calories, evening_calories):
    total_salad_calories = morning_calories + evening_calories
    surplus_deficit = calories - total_salad_calories
    return surplus_deficit

# Generate a descriptive PDF
def generate_pdf(plan):
    pdf = FPDF(orientation='P', unit='mm', format='A4')  # Portrait mode
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title Page
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.set_text_color(0, 102, 204)  # Blue text
    pdf.cell(0, 10, "10-Day Personalized Salad Plan", ln=True, align="C")
    pdf.ln(20)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "This plan includes carefully selected salads to meet your daily calorie and nutritional goals. "
                          "Each day's plan is designed for both morning and evening meals.", align="C")
    pdf.ln(10)

    # Add daily salad plans
    for idx, row in plan.iterrows():
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=14)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 10, f"Day {row['Day']}", ln=True)
        pdf.ln(10)

        # Morning Salad
        pdf.set_font("Arial", style="B", size=12)
        pdf.set_text_color(34, 139, 34)  # Green for morning
        pdf.cell(0, 10, "Morning Salad:", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 10, f"Name: {row['Morning Salad']}")
        pdf.multi_cell(0, 10, f"Quantity: {row['Morning Quantity']}")
        pdf.multi_cell(0, 10, f"Calories: {row['Morning Calories']} kcal")
        pdf.multi_cell(0, 10, f"Protein: {row['Morning Protein (g)']} g")
        pdf.ln(5)

        # Evening Salad
        pdf.set_font("Arial", style="B", size=12)
        pdf.set_text_color(220, 20, 60)  # Crimson for evening
        pdf.cell(0, 10, "Evening Salad:", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 10, f"Name: {row['Evening Salad']}")
        pdf.multi_cell(0, 10, f"Quantity: {row['Evening Quantity']}")
        pdf.multi_cell(0, 10, f"Calories: {row['Evening Calories']} kcal")
        pdf.multi_cell(0, 10, f"Protein: {row['Evening Protein (g)']} g")
        pdf.ln(5)

        # Calorie Surplus/Deficit
        pdf.set_font("Arial", style="B", size=12)
        pdf.set_text_color(128, 0, 128)  # Purple for surplus/deficit
        surplus_deficit = row['Calorie Surplus/Deficit']
        pdf.cell(0, 10, "Calorie Balance:", ln=True)
        pdf.set_font("Arial", size=10)
        if surplus_deficit > 0:
            pdf.multi_cell(0, 10, f"Surplus: {surplus_deficit:.2f} kcal")
        elif surplus_deficit < 0:
            pdf.multi_cell(0, 10, f"Deficit: {abs(surplus_deficit):.2f} kcal")
        else:
            pdf.multi_cell(0, 10, "Balanced")
        pdf.ln(10)

    pdf.ln(5)
    pdf.set_font("Arial", style="I", size=10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, "Generated with Streamlit for personal use only.", ln=True, align="C")

    return pdf.output(dest="S").encode("latin1")

# Streamlit app
def main():
    st.title("Daily Salad Planner")

    # Load salad data
    salad_data = load_data()

    # Check for required columns
    required_columns = ["Name", "Quantities", "Kcal", "Protein Content (g)"]
    if not all(col in salad_data.columns for col in required_columns):
        st.error(f"The following columns are missing: {set(required_columns) - set(salad_data.columns)}")
        return

    # User input for daily calories
    calories = st.number_input("Enter your daily calorie target (kcal):", min_value=0)

    # Plan for 10 days
    if st.button("Generate Plan for 10 Days"):
        plan = []
        for day in range(1, 11):
            morning_salad, evening_salad = get_random_salads(salad_data)
            surplus_deficit = calculate_surplus_deficit(
                calories,
                morning_salad["Kcal"],
                evening_salad["Kcal"]
            )
            plan.append({
                "Day": day,
                "Morning Salad": morning_salad["Name"],
                "Morning Quantity": morning_salad["Quantities"],
                "Morning Calories": morning_salad["Kcal"],
                "Morning Protein (g)": morning_salad["Protein Content (g)"],
                "Evening Salad": evening_salad["Name"],
                "Evening Quantity": evening_salad["Quantities"],
                "Evening Calories": evening_salad["Kcal"],
                "Evening Protein (g)": evening_salad["Protein Content (g)"],
                "Calorie Surplus/Deficit": surplus_deficit
            })

        # Create DataFrame for display
        plan_df = pd.DataFrame(plan)
        st.write(plan_df)

        # Generate and download the PDF
        pdf_content = generate_pdf(plan_df)
        st.download_button(
            label="Download Plan as PDF",
            data=pdf_content,
            file_name="salad_plan.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
