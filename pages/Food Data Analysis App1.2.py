import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset from the specified path
file_path = '/data/INDB_my.csv'

st.title("Food Data Analysis App")
st.write("Analyzing food nutritional data from the preloaded dataset.")

# Check if the file exists and read it
try:
    df = pd.read_csv(file_path)
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
        "calcium_mg",
        "phosphorus_mg",
        "potassium_mg",
    ]

    # Nutritional values per 100 grams
    st.write("### Per 100 Grams")
    nutrient_values_100g = selected_data[nutrients]
    st.write(nutrient_values_100g)

    fig_100g = px.bar(
        x=nutrients,
        y=nutrient_values_100g,
        labels={"x": "Nutrient", "y": "Amount per 100g"},
        title=f"Nutritional Breakdown (Per 100g) for {food_item}",
    )
    st.plotly_chart(fig_100g)

    # Nutritional values per serving size
    st.write("### Per Serving Size")
    nutrients_serving = [
        f"unit_serving_{nutrient}" for nutrient in nutrients
    ]
    nutrient_values_serving = selected_data[nutrients_serving].values
    nutrients_serving_labels = [nutrient.replace("unit_serving_", "") for nutrient in nutrients_serving]

    # Create a DataFrame for serving size values
    serving_df = pd.DataFrame(
        {
            "Nutrient": nutrients_serving_labels,
            "Amount per Serving": nutrient_values_serving,
        }
    )
    st.write(serving_df)

    fig_serving = px.bar(
        serving_df,
        x="Nutrient",
        y="Amount per Serving",
        labels={"x": "Nutrient", "y": "Amount per Serving"},
        title=f"Nutritional Breakdown (Per Serving) for {food_item}",
    )
    st.plotly_chart(fig_serving)

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

except FileNotFoundError:
    st.error(f"The file at {file_path} does not exist. Please ensure the path is correct.")
