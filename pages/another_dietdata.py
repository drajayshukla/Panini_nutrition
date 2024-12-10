import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Load the CSV data
@st.cache_data
def load_data():
    data = pd.read_csv("/Users/dr.ajayshukla/Downloads/newdatadiet.csv")  # Replace with your CSV file
    return data


# App title
st.title("Nutrition Data Analysis")

# Load data
data = load_data()

# Display data
st.subheader("Dataset")
st.dataframe(data)

# Sidebar filters
st.sidebar.header("Filters")

# Food Search
search_term = st.sidebar.text_input("Search Food Name", "")
if search_term:
    filtered_data = data[data['food_name'].str.contains(search_term, case=False, na=False)]
    st.subheader(f"Search Results for '{search_term}'")
    st.dataframe(filtered_data)
else:
    filtered_data = data

# Nutrient Filter
st.sidebar.subheader("Nutrient Filter")
nutrient = st.sidebar.selectbox("Select a Nutrient", data.select_dtypes(include=['float64', 'int64']).columns)
threshold = st.sidebar.number_input(f"Minimum {nutrient} value", value=0.0)
filtered_nutrient_data = filtered_data[filtered_data[nutrient] >= threshold]

# Display filtered data
st.subheader(f"Foods with {nutrient} ≥ {threshold}")
st.dataframe(filtered_nutrient_data)

# Visualization
st.sidebar.subheader("Visualization")
selected_foods = st.sidebar.multiselect("Select Food Items for Comparison", filtered_nutrient_data['food_name'])

if selected_foods:
    nutrient_data = filtered_nutrient_data[filtered_nutrient_data['food_name'].isin(selected_foods)]
    st.subheader(f"Nutrient Comparison for: {', '.join(selected_foods)}")

    # Plotting
    fig, ax = plt.subplots()
    nutrient_data.set_index('food_name')[nutrient].plot(kind='bar', ax=ax)
    ax.set_title(f"{nutrient} Levels in Selected Foods")
    ax.set_ylabel(nutrient)
    ax.set_xlabel("Food Items")
    st.pyplot(fig)

# Summary statistics
if st.sidebar.checkbox("Show Summary Statistics"):
    st.subheader("Summary Statistics")
    st.write(data.describe())
