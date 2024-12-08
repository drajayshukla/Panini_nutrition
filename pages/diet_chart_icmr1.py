import streamlit as st
import pandas as pd
import random

# Load the dataset
data_path = "data/cleaned_food_data.csv"  # Update with your file path
food_data = pd.read_csv(data_path)

# Ensure numerical columns for calculation
food_data['energy_kcal'] = pd.to_numeric(food_data['energy_kcal'], errors='coerce')
food_data.dropna(subset=['energy_kcal'], inplace=True)


# Filter foods based on preference
def filter_by_preference(data, preference):
    if preference == "Vegetarian":
        return data[data['tags'].str.contains("vegetarian", case=False, na=False)]
    elif preference == "Non-Vegetarian":
        return data[~data['tags'].str.contains("vegetarian", case=False, na=False)]
    elif preference == "Eggetarian":
        return data[data['tags'].str.contains("eggetarian", case=False, na=False)]
    else:
        return data


# Function to create a single day's diet
def create_daily_diet(filtered_data, target_calories):
    daily_diet = []
    total_calories = 0
    while total_calories < target_calories:
        # Randomly select a food item
        food_item = filtered_data.sample(1).iloc[0]
        food_name = food_item['food_name']
        food_calories = food_item['energy_kcal']

        # Add to daily diet if it doesn't exceed target
        if total_calories + food_calories <= target_calories:
            daily_diet.append((food_name, food_calories))
            total_calories += food_calories

    return daily_diet, total_calories


# Generate a 10-day diet chart
def generate_diet_chart(filtered_data, target_calories):
    diet_chart = []
    for day in range(1, 11):
        daily_diet, total_calories = create_daily_diet(filtered_data, target_calories)
        diet_chart.append((f"Day {day}", daily_diet, total_calories))
    return diet_chart


# Streamlit app
st.title("10-Day Diet Chart Generator with Preferences")
st.header("Plan your diet based on calorie requirements and food preferences")

# User input for daily calorie requirement
daily_calories = st.number_input("Enter your daily calorie requirement (kcal):", min_value=500, max_value=5000, step=50)

# User input for dietary preference
preference = st.radio(
    "Select your dietary preference:",
    ["Vegetarian", "Non-Vegetarian", "Eggetarian", "No Preference"]
)

# Filter data based on preference
filtered_data = filter_by_preference(food_data, preference)

if st.button("Generate Diet Chart"):
    if filtered_data.empty:
        st.error("No foods match your preferences. Please select a different preference.")
    else:
        diet_chart = generate_diet_chart(filtered_data, daily_calories)

        st.header("Your 10-Day Diet Chart")
        for day, daily_diet, total_calories in diet_chart:
            st.subheader(day)
            st.write(f"Total Calories: {total_calories} kcal")
            for food_name, food_calories in daily_diet:
                st.write(f"- {food_name}: {food_calories:.2f} kcal")
            st.write("---")

st.sidebar.info(
    "This tool is powered by Streamlit and uses a comprehensive food dataset to create a personalized diet plan.")
