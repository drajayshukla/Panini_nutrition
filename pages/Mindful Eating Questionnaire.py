import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from docx import Document
from docx.shared import Inches
import tempfile

# Define questionnaire sections and questions
questionnaire = {
    "Awareness": [
        "I notice when I’m full and stop eating.",
        "I pay attention to the flavors and textures of my food while eating.",
        "I eat slowly and savor each bite.",
        "I am aware of how different foods affect my body and energy levels.",
        "I focus solely on my food without distractions like TV or phone."
    ],
    "Emotional Eating": [
        "I eat when I feel stressed.",
        "I eat when I’m bored, even if I’m not hungry.",
        "I eat to cope with negative emotions, such as sadness or anger.",
        "I crave certain foods when I’m upset.",
        "I feel guilty after eating when I wasn’t truly hungry."
    ],
    "Disinhibition": [
        "I find it hard to stop eating even when I’m full.",
        "I eat more when I’m at social gatherings or parties.",
        "I eat past the point of fullness because the food tastes good.",
        "I have difficulty controlling how much I eat of certain foods (e.g., sweets, chips)."
    ],
    "External Cues": [
        "I eat just because food is available, not because I’m hungry.",
        "I eat more when I see others eating.",
        "I eat because it’s 'time to eat,' even if I’m not hungry.",
        "I eat more when I see advertisements or photos of food."
    ],
    "Hunger and Satiety": [
        "I eat only when I’m physically hungry.",
        "I stop eating when I feel satisfied, not overly full.",
        "I can distinguish between physical hunger and emotional hunger."
    ],
    "Eating Environment": [
        "I ensure my meals are eaten in a calm and relaxing environment.",
        "I set aside time specifically for eating without multitasking.",
        "I prefer eating meals at a dining table rather than on the couch or in bed."
    ]
}

# Scoring options
options = ["Always", "Often", "Sometimes", "Rarely", "Never"]

def calculate_section_scores(responses):
    return {section: sum(1 for answer in answers if answer in ["Always", "Often"]) for section, answers in responses.items()}

def visualize_radar_chart(section_scores):
    categories = list(section_scores.keys())
    values = list(section_scores.values())
    values += values[:1]  # Repeat the first value to close the circle

    num_vars = len(categories)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories, color='grey', size=10)
    ax.plot(angles, values, linewidth=2, linestyle='solid', color='blue')
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.set_title("Mindful Eating Radar Chart", size=15)
    return fig

def save_to_word(responses, section_scores, radar_chart_path):
    doc = Document()
    doc.add_heading("Mindful Eating Questionnaire (MEQ) Results", level=1)
    doc.add_paragraph("Below are your responses and a radar chart visualization based on the MEQ.")

    # Add responses
    doc.add_heading("Your Responses", level=2)
    for section, answers in responses.items():
        doc.add_heading(section, level=3)
        for question, answer in zip(questionnaire[section], answers):
            doc.add_paragraph(f"{question}: {answer}")

    # Add radar chart
    doc.add_heading("Radar Chart", level=2)
    doc.add_picture(radar_chart_path, width=Inches(4.0))

    # Save document to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(temp_file.name)
    return temp_file.name

def main():
    st.title("Mindful Eating Questionnaire (MEQ)")

    st.markdown("""
    **Purpose:**  
    This questionnaire assesses your mindfulness during meals. Select the option that best describes your behavior for each statement.
    """)

    # User responses
    responses = {}

    for section, questions in questionnaire.items():
        st.header(section)
        responses[section] = []
        for question in questions:
            response = st.selectbox(question, options, key=f"{section}_{question}")
            responses[section].append(response)

    if st.button("Submit Responses"):
        section_scores = calculate_section_scores(responses)

        # Radar Chart Visualization
        fig = visualize_radar_chart(section_scores)
        st.pyplot(fig)

        # Save radar chart as an image
        radar_chart_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
        fig.savefig(radar_chart_path, bbox_inches="tight")

        # Save to Word Document
        word_file = save_to_word(responses, section_scores, radar_chart_path)
        st.success("Word document with radar chart generated successfully!")
        with open(word_file, "rb") as file:
            st.download_button("Download Results as Word Document", file, file_name="Mindful_Eating_Results.docx")

if __name__ == "__main__":
    main()
