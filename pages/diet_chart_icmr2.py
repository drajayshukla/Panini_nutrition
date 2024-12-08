import streamlit as st
import pandas as pd
import random

# Load the dataset
data_path = "cleaned_food_data.csv"  # Update with your file path
food_data = pd.read_csv(data_path)

# Ensure numerical columns for calculations
for col in ['energy_kcal', 'protein', 'carbohydrate', 'total_fat']:
    food_data[col] = pd.to_numeric(food_data[col], errors='coerce')
food_data.dropna(subset=['energy_kcal', 'protein', 'carbohydrate', 'total_fat'], inplace=True)


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


# Function to create a single day's meal plan
def create_meal_plan(filtered_data, target_calories, macro_ratios):
    meals = {"Breakfast": 0.25, "Lunch": 0.35, "Snacks": 0.15, "Dinner": 0.25}
    daily_plan = {}
    total_macros = {"carbohydrate": 0, "protein": 0, "total_fat": 0, "calories": 0}

    for meal, proportion in meals.items():
        meal_target_calories = target_calories * proportion
        meal_plan = []
        meal_calories = 0
        meal_macros = {"carbohydrate": 0, "protein": 0, "total_fat": 0}

        while meal_calories < meal_target_calories:
            # Randomly select a food item
            food_item = filtered_data.sample(1).iloc[0]
            food_name = food_item['food_name']
            food_calories = food_item['energy_kcal']
            food_macros = {
                "carbohydrate": food_item['carbohydrate'],
                "protein": food_item['protein'],
                "total_fat": food_item['total_fat']
            }

            # Add to the meal plan if it doesn't exceed the target
            if meal_calories + food_calories <= meal_target_calories:
                meal_plan.append((food_name, food_calories, food_macros))
                meal_calories += food_calories
                for key in meal_macros:
                    meal_macros[key] += food_macros[key]

        daily_plan[meal] = meal_plan
        total_macros["calories"] += meal_calories
        for key in meal_macros:
            total_macros[key] += meal_macros[key]

    # Adjust macros to meet the target ratio
    for macro in ["carbohydrate", "protein", "total_fat"]:
        total_macros[macro] = round(total_macros[macro] / total_macros["calories"] * 100, 2)

    return daily_plan, total_macros


# Generate a 10-day diet chart
def generate_diet_chart(filtered_data, target_calories, macro_ratios):
    diet_chart = []
    for day in range(1, 11):
        daily_plan, total_macros = create_meal_plan(filtered_data, target_calories, macro_ratios)
        diet_chart.append((f"Day {day}", daily_plan, total_macros))
    return diet_chart


# Streamlit app
st.title("10-Day Diet Chart Generator with Meal Timings and Macronutrient Goals")
st.header("Plan your diet based on calorie requirements, meal timings, and macronutrient goals")

# User input for daily calorie requirement
daily_calories = st.number_input("Enter your daily calorie requirement (kcal):", min_value=500, max_value=5000, step=50)

# User input for dietary preference
preference = st.radio(
    "Select your dietary preference:",
    ["Vegetarian", "Non-Vegetarian", "Eggetarian", "No Preference"]
)

# User input for macronutrient goals
st.subheader("Set Macronutrient Proportions (in %)")
carb_ratio = st.slider("Carbohydrates (%)", 0, 100, 50)
protein_ratio = st.slider("Proteins (%)", 0, 100, 30)
fat_ratio = st.slider("Fats (%)", 0, 100, 20)

if carb_ratio + protein_ratio + fat_ratio != 100:
    st.error("Macronutrient proportions must add up to 100%.")
else:
    # Filter data based on preference
    filtered_data = filter_by_preference(food_data, preference)

    if st.button("Generate Diet Chart"):
        if filtered_data.empty:
            st.error("No foods match your preferences. Please select a different preference.")
        else:
            macro_ratios = {"carbohydrate": carb_ratio, "protein": protein_ratio, "total_fat": fat_ratio}
            diet_chart = generate_diet_chart(filtered_data, daily_calories, macro_ratios)

            st.header("Your 10-Day Diet Chart")
            for day, daily_plan, total_macros in diet_chart:
                st.subheader(day)
                st.write(f"Total Calories: {daily_calories} kcal")
                st.write(f"Macronutrient Distribution: {total_macros}")
                for meal, items in daily_plan.items():
                    st.write(f"**{meal}**")
                    for food_name, food_calories, food_macros in items:
                        st.write(f"- {food_name}: {food_calories:.2f} kcal, {food_macros}")
                    st.write("---")
