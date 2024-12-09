import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# App title
st.title("Recipe Manager and Visualizer")

# Upload file
uploaded_file = st.file_uploader("Upload your recipe CSV file", type=["csv"])
if uploaded_file:
    data = load_data(uploaded_file)

    # Show the dataset
    st.header("Dataset Preview")
    st.dataframe(data)

    # Filter options
    st.sidebar.header("Filter Recipes")
    cuisine_filter = st.sidebar.multiselect("Select Cuisine", options=data["Cuisine"].unique(), default=data["Cuisine"].unique())
    course_filter = st.sidebar.multiselect("Select Course", options=data["Course"].unique(), default=data["Course"].unique())
    diet_filter = st.sidebar.multiselect("Select Diet", options=data["Diet"].unique(), default=data["Diet"].unique())

    # Apply filters
    filtered_data = data[
        (data["Cuisine"].isin(cuisine_filter)) &
        (data["Course"].isin(course_filter)) &
        (data["Diet"].isin(diet_filter))
    ]

    st.subheader("Filtered Recipes")
    st.write(f"Showing {len(filtered_data)} recipes")
    st.dataframe(filtered_data[["RecipeName", "TranslatedRecipeName", "Cuisine", "Course", "Diet", "PrepTimeInMins", "CookTimeInMins", "TotalTimeInMins"]])

    # Recipe details
    st.subheader("View Recipe Details")
    recipe_choice = st.selectbox("Select a recipe to view details", options=filtered_data["RecipeName"])
    selected_recipe = filtered_data[filtered_data["RecipeName"] == recipe_choice].iloc[0]

    st.markdown(f"### {selected_recipe['RecipeName']} ({selected_recipe['TranslatedRecipeName']})")
    st.markdown(f"**Cuisine**: {selected_recipe['Cuisine']}")
    st.markdown(f"**Course**: {selected_recipe['Course']}")
    st.markdown(f"**Diet**: {selected_recipe['Diet']}")
    st.markdown(f"**Servings**: {selected_recipe['Servings']}")
    st.markdown(f"**Prep Time**: {selected_recipe['PrepTimeInMins']} mins")
    st.markdown(f"**Cook Time**: {selected_recipe['CookTimeInMins']} mins")
    st.markdown(f"**Total Time**: {selected_recipe['TotalTimeInMins']} mins")
    st.markdown(f"**Ingredients**: {selected_recipe['Ingredients']}")
    st.markdown(f"**Instructions**: {selected_recipe['Instructions']}")
    st.markdown(f"[View Full Recipe]({selected_recipe['URL']})")

    # Visualization
    st.header("Visualizations")

    # Cuisine distribution
    st.subheader("Cuisine Distribution")
    cuisine_counts = filtered_data["Cuisine"].value_counts().reset_index()
    cuisine_counts.columns = ["Cuisine", "Count"]
    fig_cuisine = px.bar(cuisine_counts, x="Cuisine", y="Count", title="Cuisine Distribution", text="Count")
    st.plotly_chart(fig_cuisine)

    # Time analysis
    st.subheader("Time Analysis")
    fig_time = px.scatter(filtered_data, x="PrepTimeInMins", y="CookTimeInMins",
                          size="TotalTimeInMins", color="Cuisine",
                          hover_data=["RecipeName"], title="Prep Time vs Cook Time")
    st.plotly_chart(fig_time)

    # Cuisine vs Total Time
    st.subheader("Average Total Time by Cuisine")
    avg_time_by_cuisine = filtered_data.groupby("Cuisine")["TotalTimeInMins"].mean().reset_index()
    fig_avg_time = px.bar(avg_time_by_cuisine, x="Cuisine", y="TotalTimeInMins", title="Average Total Time by Cuisine", text="TotalTimeInMins")
    st.plotly_chart(fig_avg_time)
else:
    st.info("Please upload a CSV file to get started!")
