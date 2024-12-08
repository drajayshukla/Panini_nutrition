import streamlit as st

def main():
    st.title("Food Frequency Questionnaire (FFQ)")

    st.markdown("""
    **Instructions:**
    * Please indicate how often you consume the following foods using the scale below:
        - **Never:** 0 times
        - **Rarely:** 1–3 times/month
        - **Sometimes:** 1–2 times/week
        - **Often:** 3–4 times/week
        - **Always:** Daily
    """)

    sections = {
        "Fruits and Vegetables": [
            "How often do you eat fresh fruits (e.g., apples, bananas, oranges)?",
            "How often do you eat dried fruits (e.g., raisins, dates)?",
            "How often do you eat green leafy vegetables (e.g., spinach, kale)?",
            "How often do you eat starchy vegetables (e.g., potatoes, sweet potatoes)?",
            "How often do you eat cruciferous vegetables (e.g., broccoli, cauliflower)?"
        ],
        "Grains and Cereals": [
            "How often do you consume whole grains (e.g., brown rice, oats, quinoa)?",
            "How often do you consume refined grains (e.g., white bread, pasta)?",
            "How often do you eat breakfast cereals? Specify type:",
            "How often do you eat baked goods (e.g., cookies, muffins, cakes)?"
        ],
        "Protein Sources": [
            "How often do you consume red meat (e.g., beef, lamb)?",
            "How often do you eat poultry (e.g., chicken, turkey)?",
            "How often do you eat fish or seafood?",
            "How often do you consume eggs?",
            "How often do you eat plant-based proteins (e.g., lentils, chickpeas, tofu)?"
        ],
        "Dairy and Alternatives": [
            "How often do you drink milk? Specify type (e.g., cow's milk, almond milk):",
            "How often do you eat cheese?",
            "How often do you eat yogurt? Specify type (e.g., Greek, low-fat):",
            "How often do you consume dairy-free alternatives (e.g., soy milk, oat milk)?"
        ],
        "Snacks and Beverages": [
            "How often do you eat salty snacks (e.g., chips, pretzels)?",
            "How often do you eat sugary snacks (e.g., chocolate, candy)?",
            "How often do you drink sugary beverages (e.g., soda, juice)?",
            "How often do you drink caffeinated beverages (e.g., coffee, tea)?",
            "How often do you consume alcohol? Specify type:"
        ],
        "Fats and Oils": [
            "How often do you use butter or margarine?",
            "How often do you use cooking oils? Specify type (e.g., olive, coconut):",
            "How often do you consume high-fat condiments (e.g., mayonnaise, salad dressings)?"
        ],
        "Eating Habits": [
            "How often do you eat meals prepared at home?",
            "How often do you eat meals from restaurants or takeaways?",
            "How often do you skip breakfast?",
            "How often do you snack between meals?"
        ],
        "Special Foods": [
            "How often do you consume organic foods?",
            "How often do you eat fortified foods (e.g., vitamin D-enriched milk)?",
            "How often do you eat fast foods (e.g., burgers, pizzas)?",
            "How often do you consume cultural or traditional dishes? Specify:"
        ],
        "Supplements": [
            "How often do you take multivitamins?",
            "How often do you take omega-3 or fish oil supplements?",
            "How often do you take protein supplements (e.g., whey, plant protein)?",
            "Do you use meal replacement products (e.g., shakes, bars)? How often?"
        ]
    }

    responses = {}
    for section, questions in sections.items():
        st.header(section)
        responses[section] = []
        for question in questions:
            response = st.radio(
                question,
                ("Never", "Rarely", "Sometimes", "Often", "Always", "Other"),
                index=0
            )
            remark = ""
            if response == "Other":
                remark = st.text_input(f"Remarks for '{question}':", "")
            responses[section].append({"question": question, "response": response, "remark": remark})

    if st.button("Submit"):
        st.success("Thank you for completing the questionnaire!")
        st.write("Your responses:")
        st.json(responses)

if __name__ == "__main__":
    main()
