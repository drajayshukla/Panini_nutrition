import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# App title
st.title("Food Data Analysis App")
st.write("Upload a CSV file to analyze and visualize food data.")

# Upload file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    # Load the data
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(df.head())

    # Display summary statistics
    st.write("### Summary Statistics")
    st.write(df.describe())

    # Column selection for analysis
    st.write("### Choose Columns for Analysis")
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    selected_column = st.selectbox("Select a column to visualize", numeric_columns)

    # Plot options
    st.write("### Visualization Options")
    plot_type = st.selectbox(
        "Select plot type", ["Bar Plot", "Scatter Plot", "Box Plot", "Word Cloud"]
    )

    if plot_type == "Bar Plot":
        st.write(f"### Bar Plot of {selected_column}")
        fig, ax = plt.subplots()
        df[selected_column].value_counts().plot(kind="bar", ax=ax)
        st.pyplot(fig)

    elif plot_type == "Scatter Plot":
        x_col = st.selectbox("Select X-axis", numeric_columns)
        y_col = st.selectbox("Select Y-axis", numeric_columns)
        st.write(f"### Scatter Plot of {x_col} vs {y_col}")
        fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
        st.plotly_chart(fig)

    elif plot_type == "Box Plot":
        st.write(f"### Box Plot of {selected_column}")
        fig = px.box(df, y=selected_column, title=f"Box Plot of {selected_column}")
        st.plotly_chart(fig)

    elif plot_type == "Word Cloud":
        st.write("### Word Cloud of Food Names")
        wordcloud = WordCloud(
            width=800, height=400, background_color="white"
        ).generate(" ".join(df["food_name"]))
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

    # Correlation Heatmap
    st.write("### Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df[numeric_columns].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
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
