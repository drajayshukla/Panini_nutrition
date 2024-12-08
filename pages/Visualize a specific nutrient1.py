import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned dataset
data_path = 'data/cleaned_food_data.csv'
food_data = pd.read_csv(data_path)

# Streamlit app title
st.title("Food Nutrient Explorer")

# Display the dataset
if st.checkbox("Show Raw Data"):
    st.write(food_data)

# Data Overview
st.header("Data Overview")
st.write(food_data.describe())

# Filter by nutrient range
st.header("Filter Food Items")
energy_range = st.slider("Select Energy Range (kcal)", 0, int(food_data['energy_kcal'].max()), (0, 500))
protein_range = st.slider("Select Protein Range (g)", 0, int(food_data['protein'].max()), (0, 50))

filtered_data = food_data[
    (food_data['energy_kcal'] >= energy_range[0]) &
    (food_data['energy_kcal'] <= energy_range[1]) &
    (food_data['protein'] >= protein_range[0]) &
    (food_data['protein'] <= protein_range[1])
]
st.write("Filtered Data:", filtered_data)

# Visualization: Nutrient Distribution
st.header("Nutrient Distribution")
nutrient = st.selectbox("Select a Nutrient for Visualization", ['energy_kcal', 'protein', 'iron_(fe)', 'calcium_(ca)'])
st.bar_chart(food_data.groupby('food_group')[nutrient].mean())

# Search by food name
st.header("Search Food Items")
search_query = st.text_input("Enter food name or group:")
if search_query:
    search_results = food_data[
        food_data['food_name'].str.contains(search_query, case=False, na=False) |
        food_data['food_group'].str.contains(search_query, case=False, na=False)
    ]
    st.write("Search Results:", search_results)
