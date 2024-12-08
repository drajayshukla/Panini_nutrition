import streamlit as st
import pandas as pd
import random

# Load the dataset
data_path = "data/cleaned_food_data.csv"  # Update with your file path
food_data = pd.read_csv(data_path)

# Ensure numerical columns for calculation
food_data['energy_kcal'] = pd.to_numeric(food_data['energy_kcal'], errors='coerce')
food_data.dropna(subset=['energy_kcal'], inplace=True)


# Function to create a single day's diet
def create_daily_diet(target_calories):
    daily_diet = []
    total_calories = 0
    while total_calories < target_calories:
        # Randomly select a food item
        food_item = food_data.sample(1).iloc[0]
        food_name = food_item['food_name']
        food_calories = food_item['energy_kcal']

        # Add to daily diet if it doesn't exceed target
        if total_calories + food_calories <= target_calories:
            daily_diet.append((food_name, food_calories))
            total_calories += food_calories

    return daily_diet, total_calories


# Generate a 10-day diet chart
def generate_diet_chart(target_calories):
    diet_chart = []
    for day in range(1, 11):
        daily_diet, total_calories = create_daily_diet(target_calories)
        diet_chart.append((f"Day {day}", daily_diet, total_calories))
    return diet_chart


# Streamlit app
st.title("10-Day Diet Chart Generator")
st.header("Plan your diet based on calorie requirements")

# User input for daily calorie requirement
daily_calories = st.number_input("Enter your daily calorie requirement (kcal):", min_value=500, max_value=5000, step=50)

if st.button("Generate Diet Chart"):
    diet_chart = generate_diet_chart(daily_calories)

    st.header("Your 10-Day Diet Chart")
    for day, daily_diet, total_calories in diet_chart:
        st.subheader(day)
        st.write(f"Total Calories: {total_calories} kcal")
        for food_name, food_calories in daily_diet:
            st.write(f"- {food_name}: {food_calories:.2f} kcal")
        st.write("---")

st.sidebar.info(
    "This tool is powered by Streamlit and uses a comprehensive food dataset to create a personalized diet plan.")
