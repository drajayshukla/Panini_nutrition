import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile


def save_to_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Food Diary Summary", ln=True, align="C")
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

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name


def main():
    st.title("Interactive Food Diary")

    st.markdown("""
    **Purpose:**
    This interactive food diary helps you track your meals in a fun and intuitive way!

    **Instructions:**
    1. Choose the number of days you want to log (1–3).
    2. For each day, click on the dropdown to log your meals/snacks.
    3. Add as many entries as you want for each day using the "Add Entry" tab.
    4. Upload images of packaged food labels (optional).
    5. Generate a PDF summary at the end.
    """)

    num_days = st.selectbox("How many days would you like to log?", [1, 2, 3])
    days = [f"Day {i}" for i in range(1, num_days + 1)]
    diary_data = {day: [] for day in days}

    for day in days:
        with st.expander(f"Log Meals for {day}"):
            tabs = st.tabs(["Add Entry", "Review Entries"])
            with tabs[0]:
                entries = []
                entry_id = 1

                if st.button(f"Add Entry for {day}", key=f"add_button_{day}"):
                    time = st.time_input(f"Time ({entry_id}):", key=f"{day}_time_{entry_id}")
                    food_drink = st.text_input(f"Food/Drink ({entry_id}):", key=f"{day}_food_{entry_id}")
                    portion = st.text_input(f"Portion Size ({entry_id}):", key=f"{day}_portion_{entry_id}")
                    preparation = st.text_input(f"Preparation Method ({entry_id}):", key=f"{day}_prep_{entry_id}")
                    location = st.text_input(f"Location ({entry_id}):", key=f"{day}_location_{entry_id}")
                    brand = st.text_input(f"Brand Name ({entry_id}):", key=f"{day}_brand_{entry_id}")
                    label_image = st.file_uploader(f"Upload Food Label ({entry_id}):", type=["jpg", "png"],
                                                   key=f"{day}_image_{entry_id}")

                    if food_drink:  # Only save if there's input
                        entry = {
                            "Time": time.strftime("%H:%M"),
                            "Food/Drink": food_drink,
                            "Portion": portion,
                            "Preparation": preparation,
                            "Location": location,
                            "Brand": brand,
                            "Label": label_image.name if label_image else "N/A"
                        }
                        diary_data[day].append(entry)
                        st.success(f"Entry {entry_id} added for {day}!")
                        entry_id += 1

            with tabs[1]:
                st.subheader(f"Review Entries for {day}")
                if diary_data[day]:
                    for idx, entry in enumerate(diary_data[day], 1):
                        st.write(f"**Entry {idx}:**")
                        st.write(f"- **Time:** {entry['Time']}")
                        st.write(f"- **Food/Drink:** {entry['Food/Drink']}")
                        st.write(f"- **Portion:** {entry['Portion']}")
                        st.write(f"- **Preparation:** {entry['Preparation']}")
                        st.write(f"- **Location:** {entry['Location']}")
                        st.write(f"- **Brand:** {entry['Brand']}")
                        if entry['Label'] != "N/A":
                            st.image(entry['Label'], caption=f"Food Label for Entry {idx}")
                else:
                    st.info(f"No entries logged yet for {day}.")

    if st.button("Generate PDF"):
        pdf_file = save_to_pdf(diary_data)
        st.success("PDF generated successfully!")
        with open(pdf_file, "rb") as file:
            st.download_button("Download PDF", file, file_name="Interactive_Food_Diary.pdf")


if __name__ == "__main__":
    main()
