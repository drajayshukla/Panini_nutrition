import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

def calculate_scores(responses):
    scores = {
        "High Mindful Eating": 0,
        "Moderate Mindful Eating": 0,
        "Low Mindful Eating": 0
    }

    for section, answers in responses.items():
        for response in answers:
            if response in ["Always", "Often"]:
                scores["High Mindful Eating"] += 1
            elif response == "Sometimes":
                scores["Moderate Mindful Eating"] += 1
            else:
                scores["Low Mindful Eating"] += 1
    return scores

def visualize_scores(scores):
    categories = list(scores.keys())
    values = list(scores.values())

    fig, ax = plt.subplots()
    ax.bar(categories, values, color=["green", "orange", "red"])
    ax.set_title("Mindful Eating Scores")
    ax.set_ylabel("Number of Responses")
    st.pyplot(fig)

def main():
    st.title("Mindful Eating Questionnaire (MEQ)")

    st.markdown("""
    **Purpose:**  
    This questionnaire assesses your awareness, emotional triggers, and mindfulness during meals.  
    Select the option that best describes your behavior for each statement.
    """)

    # User responses
    responses = {}

    for section, questions in questionnaire.items():
        st.header(section)
        responses[section] = []
        for question in questions:
            response = st.selectbox(question, options, key=f"{section}_{question}")
            responses[section].append(response)

    # Calculate scores and display results
    if st.button("Submit Responses"):
        scores = calculate_scores(responses)

        # Display scores
        st.subheader("Your Scores")
        st.write(scores)

        # Visualize scores
        visualize_scores(scores)

        # Provide recommendations
        st.subheader("Recommendations")
        if scores["High Mindful Eating"] >= scores["Moderate Mindful Eating"] and scores["High Mindful Eating"] >= scores["Low Mindful Eating"]:
            st.success("Great job! You have a high level of mindful eating.")
        elif scores["Moderate Mindful Eating"] > scores["High Mindful Eating"]:
            st.warning("You have a moderate level of mindful eating. Consider practicing mindful eating techniques.")
        else:
            st.error("Your mindful eating level is low. Here are some tips to improve:")
            st.write("""
            - Practice eating without distractions like TV or phones.
            - Pay attention to your hunger and satiety signals.
            - Avoid emotional eating triggers by managing stress effectively.
            """)

        # Save responses and scores as a DataFrame
        data = []
        for section, answers in responses.items():
            for question, answer in zip(questionnaire[section], answers):
                data.append({"Section": section, "Question": question, "Response": answer})
        df = pd.DataFrame(data)

        # Display the DataFrame
        st.subheader("Your Responses")
        st.dataframe(df)

        # Option to download data
        csv = df.to_csv(index=False)
        st.download_button("Download Your Responses (CSV)", csv, "responses.csv", "text/csv")

if __name__ == "__main__":
    main()
