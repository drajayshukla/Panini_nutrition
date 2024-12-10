import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# File Upload
st.title("Recipe Diet Analysis and Visualization")
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    # Read CSV file
    data = pd.read_csv(uploaded_file)
    st.dataframe(data.head())

    # 5 Best Diet Features
    st.header("Dietary Features")
    # Feature 1: Sugar content per recipe
    sugar_data = data[data["ingredient_name_org"].str.contains("Sugar", na=False)]
    sugar_per_recipe = sugar_data.groupby("recipe_name")["amount"].sum().reset_index()
    st.subheader("Sugar Content Per Recipe")
    st.bar_chart(sugar_per_recipe.set_index("recipe_name"))

    # Feature 2: Water usage per recipe
    water_data = data[data["ingredient_name_org"].str.contains("Water", na=False)]
    water_per_recipe = water_data.groupby("recipe_name")["amount"].sum().reset_index()
    st.subheader("Water Usage Per Recipe")
    st.bar_chart(water_per_recipe.set_index("recipe_name"))

    # Feature 3: Lemon usage
    lemon_data = data[data["ingredient_name_org"].str.contains("Lemon", na=False)]
    st.subheader("Recipes Using Lemon")
    st.dataframe(lemon_data[["recipe_name", "ingredient_name_org", "amount"]])

    # Feature 4: Ingredient counts
    ingredient_counts = data.groupby("recipe_name")["ingredient_name_org"].count().reset_index()
    st.subheader("Number of Ingredients Per Recipe")
    st.bar_chart(ingredient_counts.set_index("recipe_name"))

    # Feature 5: Recipes with highest caloric ingredients (assumed calorie data)
    # Simplified analysis based on sugar content for demonstration
    caloric_recipes = sugar_data.groupby("recipe_name")["amount"].sum().sort_values(ascending=False)
    st.subheader("Recipes With High Caloric Ingredients")
    st.bar_chart(caloric_recipes)

    # Visualizations
    st.header("Visualizations")
    fig, ax = plt.subplots()
    ax.pie(
        ingredient_counts["ingredient_name_org"],
        labels=ingredient_counts["recipe_name"],
        autopct='%1.1f%%',
        startangle=90
    )
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

    # Custom Search
    st.header("Custom Recipe Search")
    search_term = st.text_input("Search for a recipe or ingredient")
    if search_term:
        search_results = data[
            data["recipe_name"].str.contains(search_term, case=False, na=False) |
            data["ingredient_name_org"].str.contains(search_term, case=False, na=False)
        ]
        st.dataframe(search_results)

st.info("Upload a CSV file to get started!")
