import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px

# Load dataset
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Functions
def filter_recipes(data, cuisine=None, diet=None):
    filtered = data
    if cuisine:
        filtered = filtered[filtered['Cuisine'].str.contains(cuisine, case=False, na=False)]
    if diet:
        filtered = filtered[filtered['Diet'].str.contains(diet, case=False, na=False)]
    return filtered

def search_by_ingredients(data, ingredients):
    ingredients = [i.lower() for i in ingredients]
    return data[data['Ingredients'].str.contains('|'.join(ingredients), case=False, na=False)]

def average_cooking_time(data):
    return data[['PrepTimeInMins', 'CookTimeInMins', 'TotalTimeInMins']].mean()

def most_common_ingredients(data, n=10):
    all_ingredients = ','.join(data['Ingredients'].dropna())
    ingredient_list = [item.strip().lower() for item in all_ingredients.split(',')]
    return Counter(ingredient_list).most_common(n)

def get_top_recipes_by_time(data, n=10, shortest=True):
    sorted_data = data.sort_values('TotalTimeInMins', ascending=shortest)
    return sorted_data.head(n)

def filter_by_servings(data, min_servings, max_servings):
    return data[(data['Servings'] >= min_servings) & (data['Servings'] <= max_servings)]

def ingredient_count_distribution(data):
    data['IngredientCount'] = data['Ingredients'].apply(lambda x: len(x.split(',')) if isinstance(x, str) else 0)
    return data['IngredientCount'].value_counts()

def search_by_recipe_name(data, name):
    return data[data['RecipeName'].str.contains(name, case=False, na=False)]

def download_data(data, file_name="filtered_data.csv"):
    csv = data.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name=file_name, mime="text/csv")

def find_similar_recipes(data, ingredients):
    ingredients_set = set(ingredients.lower().split(','))
    data['Similarity'] = data['Ingredients'].apply(lambda x: len(ingredients_set & set(x.lower().split(','))) if isinstance(x, str) else 0)
    return data.sort_values(by='Similarity', ascending=False)

# Streamlit App Layout
st.title("Enhanced Recipe Explorer App")
st.sidebar.title("Options")

# Upload File
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")
if uploaded_file:
    data = load_data(uploaded_file)
    st.sidebar.success("File uploaded successfully!")

    # Tabs for functionalities
    tab = st.sidebar.selectbox(
        "Choose functionality",
        [
            "Overview", "Filter Recipes", "Search Ingredients", "Top Recipes by Time",
            "Ingredient Count Distribution", "Search by Recipe Name", "Download Data",
            "Generate Recipe Suggestions", "Visualization", "Most Popular Courses",
            "Cuisine-Ingredient Heatmap", "Recipe Similarity Search"
        ]
    )

    if tab == "Overview":
        st.header("Data Overview")
        st.write(data.head())
        st.write("**Missing Values:**")
        st.write(data.isnull().sum())
        st.write("**Average Cooking Times:**")
        st.write(average_cooking_time(data))

    elif tab == "Filter Recipes":
        st.header("Filter Recipes by Cuisine or Diet")
        cuisine = st.text_input("Enter Cuisine")
        diet = st.text_input("Enter Diet")
        filtered = filter_recipes(data, cuisine, diet)
        st.write(filtered)

    elif tab == "Search Ingredients":
        st.header("Search Recipes by Ingredients")
        ingredients = st.text_input("Enter ingredients (comma-separated)")
        if ingredients:
            ingredient_list = ingredients.split(',')
            results = search_by_ingredients(data, ingredient_list)
            st.write(results)

    elif tab == "Top Recipes by Time":
        st.header("Top Recipes by Cooking Time")
        n = st.slider("Number of recipes", 1, 20, 10)
        shortest = st.radio("Sort by", ["Shortest", "Longest"]) == "Shortest"
        st.write(get_top_recipes_by_time(data, n, shortest))

    elif tab == "Ingredient Count Distribution":
        st.header("Ingredient Count Distribution")
        counts = ingredient_count_distribution(data)
        st.bar_chart(counts)

    elif tab == "Search by Recipe Name":
        st.header("Search Recipes by Name")
        name = st.text_input("Enter recipe name")
        if name:
            st.write(search_by_recipe_name(data, name))

    elif tab == "Download Data":
        st.header("Download Filtered Data")
        st.write(data)
        download_data(data)

    elif tab == "Generate Recipe Suggestions":
        st.header("Recipe Suggestions")
        cuisine = st.text_input("Enter preferred cuisine")
        ingredients = st.text_input("Enter ingredients (comma-separated)")
        suggested = filter_recipes(data, cuisine=cuisine) if cuisine else data
        if ingredients:
            suggested = search_by_ingredients(suggested, ingredients.split(','))
        st.write(suggested)

    elif tab == "Visualization":
        viz_type = st.selectbox(
            "Choose Visualization Type",
            ["Cuisine Distribution", "Preparation vs Cooking Time", "Word Cloud for Ingredients", "Interactive Pie Chart"]
        )
        if viz_type == "Cuisine Distribution":
            st.header("Cuisine Distribution")
            plot_cuisine_distribution(data)
        elif viz_type == "Preparation vs Cooking Time":
            st.header("Preparation vs Cooking Time")
            plot_prep_vs_cook_time(data)
        elif viz_type == "Word Cloud for Ingredients":
            st.header("Word Cloud for Ingredients")
            plot_wordcloud_for_ingredients(data)
        elif viz_type == "Interactive Pie Chart":
            st.header("Interactive Cuisine Pie Chart")
            interactive_cuisine_pie_chart(data)

    elif tab == "Most Popular Courses":
        st.header("Most Popular Courses")
        st.bar_chart(data['Course'].value_counts())

    elif tab == "Cuisine-Ingredient Heatmap":
        st.header("Cuisine-Ingredient Heatmap")
        cuisine_ingredient_matrix = pd.crosstab(data['Cuisine'], data['Ingredients'].str.split(',').apply(len))
        st.write(cuisine_ingredient_matrix)

    elif tab == "Recipe Similarity Search":
        st.header("Find Similar Recipes")
        ingredients = st.text_input("Enter ingredients (comma-separated)")
        if ingredients:
            st.write(find_similar_recipes(data, ingredients))
else:
    st.sidebar.warning("Please upload a CSV file to proceed.")
