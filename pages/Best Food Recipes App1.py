import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# App title
st.title("Best Food App")
#st.write("Upload your CSV file to explore delicious food recipes and details!")
file_path = 'data/recipe_links.csv'
# Upload file
uploaded_file = file_path
# File uploader
#uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    # Load the uploaded CSV into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Display table
    st.write("### Food Details")
    st.dataframe(df, use_container_width=True)

    # Search functionality
    st.write("### Search Food")
    search_query = st.text_input("Search by food name or code (e.g., 'Sattu' or 'OSR002')")

    if search_query:
        filtered_df = df[df["Food Names"].str.contains(search_query, case=False, na=False) |
                         df["Food Code"].str.contains(search_query, case=False, na=False)]
        if not filtered_df.empty:
            st.write("#### Search Results")
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.write("No results found.")

    # Generate Word Cloud of food names
    st.write("### Food Name Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(df["Food Names"].dropna()))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # Link to recipes
    st.write("### View Recipe")
    selected_food = st.selectbox("Select a food to view its recipe", df["Food Names"])

    if selected_food:
        food_link = df[df["Food Names"] == selected_food]["Link"].values[0]
        st.write(f"Click [here]({food_link}) to view the recipe for **{selected_food}**.")
