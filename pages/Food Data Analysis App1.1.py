import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
st.title("Food Data Analysis App")
st.write("Upload a CSV file to explore and analyze food nutritional data.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Show dataset preview
    st.write("### Dataset Preview")
    st.dataframe(df.head())

    # Summary statistics
    st.write("### Summary Statistics")
    st.write(df.describe())

    # Individual food item analysis
    st.write("### Individual Food Item Analysis")
    food_item = st.selectbox("Select a food item", df["food_name"].unique())
    selected_data = df[df["food_name"] == food_item].iloc[0]

    st.write("#### Detailed Nutritional Information")
    st.write(selected_data)

    # Nutritional breakdown visualization
    st.write("#### Nutritional Breakdown")
    nutrients = [
        "energy_kcal",
        "carb_g",
        "protein_g",
        "fat_g",
        "fibre_g",
        "sfa_mg",
        "mufa_mg",
        "pufa_mg",
        "cholesterol_mg",
    ]
    nutrient_values = selected_data[nutrients]

    fig = px.bar(
        x=nutrients,
        y=nutrient_values,
        labels={"x": "Nutrient", "y": "Amount"},
        title=f"Nutritional Breakdown for {food_item}",
    )
    st.plotly_chart(fig)

    # Comparison between multiple foods
    st.write("### Compare Multiple Food Items")
    food_items = st.multiselect("Select foods to compare", df["food_name"].unique())
    if food_items:
        comparison_data = df[df["food_name"].isin(food_items)][
            ["food_name"] + nutrients
        ]
        st.write(comparison_data)

        fig = px.bar(
            comparison_data.melt(id_vars=["food_name"], var_name="Nutrient", value_name="Value"),
            x="Nutrient",
            y="Value",
            color="food_name",
            barmode="group",
            title="Nutritional Comparison",
        )
        st.plotly_chart(fig)

    # Correlation heatmap
    st.write("### Correlation Heatmap")
    corr = df[nutrients].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
