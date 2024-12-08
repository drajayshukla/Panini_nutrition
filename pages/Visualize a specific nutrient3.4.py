import streamlit as st
import pandas as pd

# Load the dataset
data_path = "cleaned_food_data.csv"  # Update with your file path
food_data = pd.read_csv(data_path)

# Ensure numerical columns for calculations
numerical_columns = food_data.select_dtypes(include=['float64', 'int64']).columns.tolist()

# Streamlit app
st.title("Top 10 Foods by Nutrient")
st.header("Identify the most nutrient-dense foods")

# Dropdown to select a nutrient
selected_nutrient = st.selectbox("Select a nutrient to rank food items:", numerical_columns)

# Filter data to exclude missing values for the selected nutrient
filtered_data = food_data.dropna(subset=[selected_nutrient])

# Sort data by the selected nutrient and get the top 10 items
top_foods = filtered_data.sort_values(by=selected_nutrient, ascending=False).head(10)

# Display the top 10 items
st.subheader(f"Top 10 Foods by {selected_nutrient.replace('_', ' ').capitalize()}")
st.write(top_foods[['food_name', 'food_group', selected_nutrient]])

# Plot a bar chart for the top 10 items
st.subheader(f"Bar Chart: Top 10 Foods by {selected_nutrient.replace('_', ' ').capitalize()}")
st.bar_chart(data=top_foods.set_index('food_name')[selected_nutrient])

# Footer
st.sidebar.info("This tool allows you to find nutrient-dense foods by specific nutrients.")
