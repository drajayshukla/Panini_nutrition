import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile


def save_to_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="One-Day Food Diary", ln=True, align="C")
    pdf.ln(10)

    for day, entries in data.items():
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt=f"Day: {day}", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        for entry in entries:
            pdf.cell(0, 10, txt=f"Time: {entry['Time']}, Food/Drink: {entry['Food/Drink']}", ln=True)
            pdf.cell(0, 10, txt=f"Portion: {entry['Portion']}, Preparation: {entry['Preparation']}", ln=True)
            pdf.cell(0, 10, txt=f"Location: {entry['Location']}, Brand: {entry['Brand']}", ln=True)
            pdf.ln(5)

    # Save PDF to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name


def main():
    st.title("One-Day Food Diary")

    st.markdown("""
    **Purpose:**
    This tool is designed to record and evaluate dietary intake over three consecutive days, including one weekend day. It provides a detailed snapshot of eating habits, portion sizes, and timing.

    **Instructions:**
    1. Record everything you eat and drink for three days, including meals, snacks, and beverages.
    2. Note the time of each intake.
    3. Specify portion sizes and preparation methods (e.g., boiled, fried, baked).
    4. Mention the location where you ate (e.g., home, office, restaurant).
    5. Include brand names if packaged foods are consumed.
    """)

    days = ["Day 1", "Day 2", "Day 3"]
    diary_data = {day: [] for day in days}

    for day in days:
        st.header(day)
        entries = []
        with st.form(key=f"form_{day}"):
            for i in range(1, 6):  # Up to 5 entries per day
                st.subheader(f"Entry {i}")
                time = st.time_input(f"Time for Entry {i} ({day}):", key=f"{day}_time_{i}")
                food_drink = st.text_input(f"Food/Drink for Entry {i} ({day}):", key=f"{day}_food_{i}")
                portion = st.text_input(f"Portion Size for Entry {i} ({day}):", key=f"{day}_portion_{i}")
                preparation = st.text_input(f"Preparation Method for Entry {i} ({day}):", key=f"{day}_prep_{i}")
                location = st.text_input(f"Location for Entry {i} ({day}):", key=f"{day}_location_{i}")
                brand = st.text_input(f"Brand Name (if any) for Entry {i} ({day}):", key=f"{day}_brand_{i}")

                if food_drink:  # Only add if there's an entry
                    entries.append({
                        "Time": time.strftime("%H:%M"),
                        "Food/Drink": food_drink,
                        "Portion": portion,
                        "Preparation": preparation,
                        "Location": location,
                        "Brand": brand
                    })

            submitted = st.form_submit_button("Save Entries for " + day)
            if submitted:
                diary_data[day] = entries
                st.success(f"Entries for {day} saved!")

    if st.button("Generate PDF"):
        pdf_file = save_to_pdf(diary_data)
        st.success("PDF generated successfully!")
        with open(pdf_file, "rb") as file:
            st.download_button("Download PDF", file, file_name="One_Day_Food_Diary.pdf")


if __name__ == "__main__":
    main()
