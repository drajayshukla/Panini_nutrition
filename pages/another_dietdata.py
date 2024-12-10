import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV data
@st.cache_data
def load_data():
    # Replace with your CSV file path
    data = pd.read_csv("data/newdatadiet.csv")
    return data

# App title
st.title("Nutrition Data Analysis")

# Load data
data = load_data()
numeric_columns = [
    "energy_kcal", "protein_g", "carb_g", "fat_g", "fibre_g", "sfa_mg", "mufa_mg",
    "pufa_mg", "cholesterol_mg", "calcium_mg", "phosphorus_mg", "magnesium_mg",
    "sodium_mg", "potassium_mg", "iron_mg", "copper_mg", "selenium_ug",
    "chromium_mg", "manganese_mg", "zinc_mg", "vitb1_mg", "vitb2_mg", "vitb3_mg",
    "vitb5_mg", "vitb6_mg", "vitb7_ug", "vitc_mg"
]

for column in numeric_columns:
    if column in data.columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")
# Data Preprocessing: Clean up column names
data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")

# Sidebar filters
st.sidebar.header("Filters")

# Search Food Name
search_term = st.sidebar.text_input("Search Food Name", "")
if search_term:
    filtered_data = data[data['food_name'].str.contains(search_term, case=False, na=False)]
else:
    filtered_data = data

# Multi-Nutrient Filters
st.sidebar.subheader("Nutrient Filters")
energy_range = st.sidebar.slider("Energy (kcal)", 0, int(data["energy_kcal"].max()), (0, 300))
protein_range = st.sidebar.slider("Protein (g)", 0, int(data["protein_g"].max()), (0, 50))

filtered_data = filtered_data[
    (filtered_data["energy_kcal"] >= energy_range[0]) &
    (filtered_data["energy_kcal"] <= energy_range[1]) &
    (filtered_data["protein_g"] >= protein_range[0]) &
    (filtered_data["protein_g"] <= protein_range[1])
]

# Display Filtered Data
st.subheader("Filtered Data")
st.dataframe(filtered_data)

# Visualization Section
st.sidebar.subheader("Visualization")
selected_foods = st.sidebar.multiselect("Select Food Items for Comparison", filtered_data['food_name'].unique())

if selected_foods:
    nutrients = st.sidebar.multiselect(
        "Select Nutrients to Compare",
        ["energy_kcal", "carb_g", "protein_g", "fat_g", "fibre_g"],
        default=["energy_kcal", "protein_g"]
    )
    if nutrients:
        comparison_data = filtered_data[filtered_data['food_name'].isin(selected_foods)]
        comparison_data = comparison_data.set_index("food_name")[nutrients]

        # Bar Chart
        st.subheader(f"Nutrient Comparison for {', '.join(selected_foods)}")
        fig, ax = plt.subplots(figsize=(10, 6))
        comparison_data.plot(kind="bar", ax=ax)
        ax.set_title("Nutrient Comparison")
        ax.set_ylabel("Values")
        ax.set_xlabel("Food Items")
        st.pyplot(fig)

# Correlation Heatmap
if st.sidebar.checkbox("Show Correlation Heatmap"):
    st.subheader("Nutrient Correlation Heatmap")
    corr_data = filtered_data.select_dtypes(include=["float64", "int64"])
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_data.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# Summary Statistics
if st.sidebar.checkbox("Show Summary Statistics"):
    st.subheader("Summary Statistics")
    st.write(filtered_data.describe())

# Download Filtered Data
st.sidebar.subheader("Download Data")
if not filtered_data.empty:
    st.download_button(
        "Download Filtered Data",
        filtered_data.to_csv(index=False),
        file_name="filtered_data.csv",
        mime="text/csv"
    )
else:
    st.sidebar.warning("No data to download. Please adjust your filters.")

# Footer
st.markdown("### Powered by Streamlit")
st.markdown(
    "This app allows you to explore, filter, and visualize nutrition data for various food items."
)
