import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px

# Load dataset
@st.cache
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

def plot_cuisine_distribution(data):
    cuisine_counts = data['Cuisine'].value_counts()
    fig, ax = plt.subplots(figsize=(12, 6))
    cuisine_counts.plot(kind='bar', ax=ax, title='Cuisine Distribution')
    st.pyplot(fig)

def plot_prep_vs_cook_time(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot.scatter(x='PrepTimeInMins', y='CookTimeInMins', alpha=0.5, ax=ax, title='Preparation vs Cooking Time')
    st.pyplot(fig)

def plot_wordcloud_for_ingredients(data):
    all_ingredients = ' '.join(data['Ingredients'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_ingredients)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

def interactive_cuisine_pie_chart(data):
    fig = px.pie(data, names='Cuisine', title='Cuisine Distribution')
    st.plotly_chart(fig)

# Streamlit App Layout
st.title("Recipe Explorer App")
st.sidebar.title("Options")

# Upload File
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")
if uploaded_file:
    data = load_data(uploaded_file)
    st.sidebar.success("File uploaded successfully!")

    # Tabs for functionalities
    tab = st.sidebar.selectbox(
        "Choose functionality",
        ["Overview", "Filter Recipes", "Search Ingredients", "Visualization"]
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

else:
    st.sidebar.warning("Please upload a CSV file to proceed.")
