import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud

# App title
st.title("Food Data Analysis App")
st.write("Upload a CSV file to analyze and visualize food data.")
file_path = 'data/INDB_my.csv'
# Upload file
uploaded_file = file_path
# Upload file
#uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    # Load the data
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(df.head())

    # Display summary statistics
    st.write("### Summary Statistics")
    st.write(df.describe())

    # Column selection for analysis
    st.write("### Choose Column for Analysis")
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    selected_column = st.selectbox("Select a column to analyze", numeric_columns)

    # Top 20 and Bottom 20 analysis
    st.write("### Top 20 and Bottom 20 Analysis")
    if selected_column:
        top_20 = df.nlargest(20, selected_column)
        bottom_20 = df.nsmallest(20, selected_column)

        st.write("#### Top 20")
        st.dataframe(top_20[["food_name", selected_column]])

        st.write("#### Bottom 20")
        st.dataframe(bottom_20[["food_name", selected_column]])

        # Visualization for Top 20
        st.write(f"### Bar Plot: Top 20 by {selected_column}")
        fig = px.bar(
            top_20,
            x="food_name",
            y=selected_column,
            labels={"food_name": "Food Name", selected_column: f"{selected_column}"},
            title=f"Top 20 Foods by {selected_column}",
        )
        st.plotly_chart(fig)

        # Visualization for Bottom 20
        st.write(f"### Bar Plot: Bottom 20 by {selected_column}")
        fig = px.bar(
            bottom_20,
            x="food_name",
            y=selected_column,
            labels={"food_name": "Food Name", selected_column: f"{selected_column}"},
            title=f"Bottom 20 Foods by {selected_column}",
        )
        st.plotly_chart(fig)

    # Correlation Heatmap
    st.write("### Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df[numeric_columns].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # Word Cloud for Food Names
    st.write("### Word Cloud of Food Names")
    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate(" ".join(df["food_name"]))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # Custom Analysis
    st.write("### Custom Analysis")
    if st.checkbox("Show Top Foods by Energy (kcal)"):
        top_foods = df.nlargest(5, "energy_kcal")[["food_name", "energy_kcal"]]
        st.write(top_foods)

    if st.checkbox("Show Nutritional Comparison"):
        selected_foods = st.multiselect("Select foods to compare", df["food_name"].unique())
        if selected_foods:
            comparison_data = df[df["food_name"].isin(selected_foods)][
                ["food_name", "energy_kcal", "protein_g", "carb_g", "fat_g"]
            ]
            st.write(comparison_data)
            fig = px.bar(
                comparison_data,
                x="food_name",
                y=["energy_kcal", "protein_g", "carb_g", "fat_g"],
                barmode="group",
                title="Nutritional Comparison",
            )
            st.plotly_chart(fig)
