import streamlit as st
import json
import pandas as pd
import random
from fpdf import FPDF
import tempfile


# Function to load JSON from a specified file path
def load_json(file_path):
    """Load JSON data from a file path."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def generate_30_day_chart(selected_items, data, calorie_limit=None):
    """Generate a 30-day randomized diet chart."""
    meals = {
        "Breakfast": ["A1", "A2", "A3"],
        "Morning Snack": ["B1", "B2"],
        "Lunch": ["C1", "C2", "C3", "C4", "C5"],
        "Evening Snack": ["D1", "D2", "D3"],
        "Dinner": ["E1", "E2", "E3", "E4", "E5"],
        "Bedtime": ["F1"]
    }

    monthly_chart = []

    for day in range(1, 31):
        daily_chart = {"Day": day}
        total_kcal = 0

        for meal, categories in meals.items():
            daily_chart[meal] = []
            for category in categories:
                if category in selected_items:
                    items = [data[category][int(index)] for index in selected_items[category]]
                    selected_item = random.choice(items)
                    daily_chart[meal].append(f"{selected_item['Name']} ({selected_item['Kcal']} Kcal)")
                    total_kcal += int(selected_item["Kcal"])

        daily_chart["Total Kcal"] = total_kcal
        if calorie_limit and total_kcal > calorie_limit:
            continue  # Skip this day if it exceeds the calorie limit
        monthly_chart.append(daily_chart)

    return pd.DataFrame(monthly_chart)


def create_pdf(monthly_chart_df):
    """Generate a PDF from the 30-day diet chart DataFrame."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="30-Day Diet Chart", ln=True, align='C')
    pdf.ln(10)  # Add a line break

    for _, row in monthly_chart_df.iterrows():
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(0, 10, f"Day {row['Day']}", ln=True)
        pdf.set_font("Arial", size=12)
        for meal, items in row.items():
            if meal not in ["Day", "Total Kcal"]:
                pdf.cell(0, 10, f"{meal}: {', '.join(items)}", ln=True)
        pdf.cell(0, 10, f"Total Calories: {row['Total Kcal']} Kcal", ln=True)
        pdf.ln(10)

    return pdf.output(dest='S').encode('latin1')  # Return as a bytes object


# Streamlit App
st.title("30-Day Diet Chart Generator")

# Specify JSON file location
file_path = "data/dietdrajaybest.json"
st.info(f"Using JSON file at: {file_path}")

# Load JSON Data
try:
    data = load_json(file_path)
    st.success("JSON file loaded successfully!")

    # Create a checklist for selection
    st.header("Select Items for Diet Chart")
    selected_items = {}
    for category, items in data.items():
        st.subheader(category)
        for index, item in enumerate(items):
            item_label = f"{item['Name']} ({item['Quantities']}, {item['Kcal']} Kcal)"
            if st.checkbox(item_label, key=f"{category}_{index}"):
                if category not in selected_items:
                    selected_items[category] = []
                selected_items[category].append(str(index))

    # Set calorie limit
    calorie_limit = st.number_input("Set a daily calorie limit (optional):", min_value=0, value=2000, step=100)

    # Generate Diet Chart
    if st.button("Generate 30-Day Diet Chart"):
        if selected_items:
            monthly_chart_df = generate_30_day_chart(selected_items, data, calorie_limit)
            st.subheader("Generated 30-Day Diet Chart")
            st.dataframe(monthly_chart_df)

            # Provide option to download as PDF
            pdf_data = create_pdf(monthly_chart_df)
            st.download_button(
                label="Download 30-Day Diet Chart as PDF",
                data=pdf_data,
                file_name="30_day_diet_chart.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("No items selected. Please select at least one item.")

except Exception as e:
    st.error(f"Error loading JSON file: {e}")
