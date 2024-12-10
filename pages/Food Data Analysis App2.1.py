import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
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
    st.write("### Choose Column for Analysis")
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    text_columns = df.select_dtypes(include=["object"]).columns.tolist()
    selected_column = st.selectbox("Select a column to analyze", numeric_columns + text_columns)

    if selected_column in text_columns:
        # Word Cloud for the selected text column
        st.write(f"### Word Cloud for '{selected_column}'")
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            " ".join(df[selected_column].dropna())
        )
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    elif selected_column in numeric_columns:
        # Correlation analysis for the selected numeric column
        st.write(f"### Correlation Analysis for '{selected_column}'")
        correlation_values = df[numeric_columns].corr()[selected_column].sort_values(ascending=False)
        st.write(correlation_values)

        # Correlation heatmap for the selected column
        st.write(f"### Correlation Heatmap for '{selected_column}'")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            df[numeric_columns].corr()[[selected_column]].sort_values(by=selected_column, ascending=False),
            annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
        )
        st.pyplot(fig)
