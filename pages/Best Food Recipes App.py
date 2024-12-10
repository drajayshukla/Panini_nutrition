import streamlit as st
import pandas as pd
import os

# App title
st.title("Best Food Recipes App")
st.write("Explore a variety of food recipes and beverages.")

# Automatically read the CSV file from the 'data' folder
file_path = 'data/recipe_links.csv' # Ensure the CSV file is placed in this folder

if os.path.exists(file_path):
    # Load the data from the file
    df = pd.read_csv(file_path)

    # Display the data
    st.write("### Food Recipes List")
    st.dataframe(df)

    # Search functionality
    st.write("### Search Food Recipes")
    food_name_search = st.text_input("Search by Food Name or Code")
    if food_name_search:
        filtered_df = df[
            df["Food Names"].str.contains(food_name_search, case=False, na=False) |
            df["Food Code"].str.contains(food_name_search, case=False, na=False)
        ]
        st.write(f"### Search Results for '{food_name_search}'")
        if not filtered_df.empty:
            st.dataframe(filtered_df)
        else:
            st.write("No recipes found.")

    # Sorted list of recipes
    st.write("### Sorted List of Food Recipes by Name")
    sorted_df = df.sort_values(by="Food Names")
    st.dataframe(sorted_df)

    # Display links for recipes
    st.write("### Recipe Links")
    for index, row in df.iterrows():
        st.write(f"**{row['Food Names']}**: [View Recipe]({row['Link']})")

    # Recipe details based on selected code
    st.write("### View Recipe Details")
    food_code = st.selectbox("Select a Food Recipe Code", df["Food Code"].unique())
    selected_recipe = df[df["Food Code"] == food_code]
    st.write(f"### Selected Recipe Details: {selected_recipe.iloc[0]['Food Names']}")
    st.write(f"**Food Code**: {selected_recipe.iloc[0]['Food Code']}")
    st.write(f"**Link**: [View Recipe]({selected_recipe.iloc[0]['Link']})")

else:
    st.error(f"The file '{file_path}' does not exist. Please ensure the file is located in the 'data' folder.")
