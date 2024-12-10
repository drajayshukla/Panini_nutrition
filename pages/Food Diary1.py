import streamlit as st
from datetime import datetime
from fpdf import FPDF
import tempfile

# Save data to PDF
def save_to_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Enhanced Food Diary", ln=True, align="C")
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
            if entry['Photo']:
                pdf.cell(0, 10, txt="Photo uploaded: Yes", ln=True)
            else:
                pdf.cell(0, 10, txt="Photo uploaded: No", ln=True)
            pdf.ln(5)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

def main():
    st.title("🍎 Fun & Engaging Food Diary 🥗")

    st.markdown("""
    **Welcome to Your Personalized Food Diary!**
    - Use emojis to select your day and record meals/snacks interactively.
    - Add photos to make it visual!
    - Track your progress with badges and a progress bar.
    """)

    days = {"🍎 Day 1": "Day 1", "🥗 Day 2": "Day 2", "🍔 Day 3": "Day 3"}
    diary_data = {day: [] for day in days.values()}
    badges = {"Day 1": "🥇", "Day 2": "🥈", "Day 3": "🥉"}

    # Select day
    st.subheader("Select the day to log:")
    selected_day = st.radio("Pick a day:", list(days.keys()))
    day_name = days[selected_day]

    # Progress bar for entries
    progress = len(diary_data[day_name]) / 5
    st.progress(progress)

    if progress == 1:
        st.success(f"Congratulations! You've logged all meals for {day_name}! {badges[day_name]}")

    # Timeline-style input
    st.subheader(f"Log Meals for {day_name}")
    if st.button("Add a Meal"):
        with st.form(key=f"form_{day_name}"):
            time = st.time_input("Meal Time:", value=datetime.now().time())
            food_drink = st.text_input("Food/Drink:")
            portion = st.text_input("Portion Size:")
            preparation = st.text_input("Preparation Method (e.g., boiled, fried):")
            location = st.text_input("Location (e.g., home, office):")
            brand = st.text_input("Brand Name (if any):")
            photo = st.file_uploader("Upload a photo of the meal (optional):", type=["jpg", "png"])

            submit = st.form_submit_button("Save Meal")
            if submit:
                diary_data[day_name].append({
                    "Time": time.strftime("%H:%M"),
                    "Food/Drink": food_drink,
                    "Portion": portion,
                    "Preparation": preparation,
                    "Location": location,
                    "Brand": brand,
                    "Photo": photo
                })
                st.success("Meal added successfully!")

    # Review meals
    st.subheader(f"Review Meals for {day_name}")
    if diary_data[day_name]:
        for idx, entry in enumerate(diary_data[day_name], 1):
            st.write(f"**Meal {idx}:**")
            st.write(f"- **Time:** {entry['Time']}")
            st.write(f"- **Food/Drink:** {entry['Food/Drink']}")
            st.write(f"- **Portion:** {entry['Portion']}")
            st.write(f"- **Preparation:** {entry['Preparation']}")
            st.write(f"- **Location:** {entry['Location']}")
            st.write(f"- **Brand:** {entry['Brand']}")
            if entry['Photo']:
                st.image(entry['Photo'], caption=f"Meal {idx} Photo")

    # Generate PDF
    if st.button("Generate PDF"):
        pdf_file = save_to_pdf(diary_data)
        st.success("PDF generated successfully!")
        with open(pdf_file, "rb") as file:
            st.download_button("Download PDF", file, file_name="Enhanced_Food_Diary.pdf")

if __name__ == "__main__":
    main()
