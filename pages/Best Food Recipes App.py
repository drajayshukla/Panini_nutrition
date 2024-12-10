import streamlit as st
import pandas as pd

# App title
st.title("Best Food Recipes App")
st.write("Explore a variety of food recipes and beverages.")

# Data for food items
data = {
    "Food Names": [
        "Woodapple juice (Bel ka sharbat)",
        "Sattu drink",
        "Apple and honey sorbet (Seb aur shehad ka sharbat)",
        "Thandai",
        "Cucumber sharbat (Kheere ka sharbat)",
        "Apple oats chia seed smoothie",
        "Nannari sharbat",
        "Semolina milk drink (Thari kanji)",
        "Saffron milk (Kesariya doodh)"
    ],
    "Food Code": [
        "OSR001",
        "OSR002",
        "OSR004",
        "OSR005",
        "OSR006",
        "OSR007",
        "OSR008",
        "OSR009",
        "OSR010"
    ],
    "Link": [
        "https://www.betterbutter.in/recipe/32734/wood-apple-bael-juice/",
        "https://www.vegrecipesofindia.com/sattu-drink-recipe-sattu-sharbat/",
        "https://www.allrecipes.com/recipe/76202/apple-and-honey-sorbet/",
        "https://www.indianhealthyrecipes.com/thandai/",
        "https://www.recipemasters.in/recipe/cucumber-sharbat/",
        "https://food.ndtv.com/recipe-apple-oats-chia-seeds-smoothie-958104",
        "https://www.sharmispassions.com/nannari-sarbath-recipe-homemade-nannari-syrup/",
        "https://mildlyindian.com/malabar-cuisine-thari-kanji-iftar-semolina-pudding/",
        "https://food.ndtv.com/recipe-kesaria-doodh-219040"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Display the data
st.write("### Food Recipes List")
st.dataframe(df)

# Filter by food name (search functionality)
food_name_search = st.text_input("Search for a Food Recipe by Name")
if food_name_search:
    filtered_df = df[df["Food Names"].str.contains(food_name_search, case=False, na=False)]
    st.write(f"### Search Results for '{food_name_search}'")
    st.dataframe(filtered_df)

# Sort the list by food name
st.write("### Sorted List of Food Recipes by Name")
sorted_df = df.sort_values(by="Food Names")
st.dataframe(sorted_df)

# Link to each recipe
st.write("### Click to View Recipe Links")
for index, row in df.iterrows():
    st.write(f"**{row['Food Names']}**: [View Recipe]({row['Link']})")

# User interaction for recipe details
food_code = st.selectbox("Select a Food Recipe Code", df["Food Code"].unique())
selected_recipe = df[df["Food Code"] == food_code]
st.write(f"### Selected Recipe Details: {selected_recipe.iloc[0]['Food Names']}")
st.write(f"**Food Code**: {selected_recipe.iloc[0]['Food Code']}")
st.write(f"**Link**: [View Recipe]({selected_recipe.iloc[0]['Link']})")
