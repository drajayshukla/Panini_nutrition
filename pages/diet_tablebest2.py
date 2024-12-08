import streamlit as st
import json
import pandas as pd
from fpdf import FPDF

# Function to load JSON from a specified file path
def load_json(file_path):
    """Load JSON data from a file path."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON file: {file_path}")
        return None

def generate_diet_chart(selected_items, data):
    """Generate a diet chart from selected items."""
    diet_chart = []
    for selection in selected_items:
        category, index = selection.split("_")
        index = int(index)
        item = data[category][index]
        diet_chart.append({
            "Category": category,
            "Name": item["Name"],
            "Quantities": item["Quantities"],
            "Kcal": item["Kcal"]
        })
    return pd.DataFrame(diet_chart)

def create_pdf_with_wrapping(diet_chart_df):
    """Generate a PDF with wrapped text in table cells."""
    class PDF(FPDF):
        def header(self):
            """Custom header for the PDF."""
            self.set_font('Arial', 'B', 14)
            self.set_fill_color(200, 220, 255)
            self.cell(0, 10, 'One Day Diet Chart', 0, 1, 'C', fill=True)
            self.ln(5)

        def footer(self):
            """Custom footer for the PDF."""
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

        def multi_cell_with_wrap(self, w, h, txt, border=0, align='L', fill=False):
            """Custom method for text wrapping within a cell."""
            self.multi_cell(w, h, txt, border=border, align=align, fill=fill)

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Add table headers with background color
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(40, 10, "Category", border=1, align='C', fill=True)
    pdf.cell(80, 10, "Name", border=1, align='C', fill=True)
    pdf.cell(40, 10, "Quantities", border=1, align='C', fill=True)
    pdf.cell(30, 10, "Kcal", border=1, align='C', fill=True)
    pdf.ln()

    # Add rows with text wrapping
    pdf.set_font("Arial", size=10)
    for index, row in diet_chart_df.iterrows():
        pdf.cell(40, 10, row["Category"], border=1)
        pdf.cell(80, 10, row["Name"], border=1)
        pdf.cell(40, 10, row["Quantities"], border=1)
        pdf.cell(30, 10, str(row["Kcal"]), border=1)
        pdf.ln()

    return pdf.output(dest='S').encode('latin1')  # Return as a bytes object

# Streamlit App
st.title("Diet Chart Generator")

# Specify JSON file location
file_path = "data/dietdrajaybest.json"
st.info(f"Using JSON file at: {file_path}")

# Load JSON Data
data = load_json(file_path)
if data:
    st.success("JSON file loaded successfully!")

    # Create a checklist for selection
    st.header("Select Items for Diet Chart")
    selected_items = []
    for category, items in data.items():
        st.subheader(category)
        for index, item in enumerate(items):
            item_label = f"{item['Name']} ({item['Quantities']}, {item['Kcal']} Kcal)"
            if st.checkbox(item_label, key=f"{category}_{index}"):
                selected_items.append(f"{category}_{index}")

    # Generate Diet Chart
    if st.button("Generate Diet Chart"):
        if selected_items:
            diet_chart_df = generate_diet_chart(selected_items, data)
            st.subheader("Generated Diet Chart")
            st.dataframe(diet_chart_df)

            # Provide option to download as PDF
            pdf_data = create_pdf_with_wrapping(diet_chart_df)
            st.download_button(
                label="Download Diet Chart as PDF",
                data=pdf_data,
                file_name="diet_chart.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("No items selected. Please select at least one item.")
else:
    st.error("Failed to load JSON data. Please check the file path and format.")
