import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data_path = "cleaned_food_data.csv"  # Update with your file path if necessary
food_data = pd.read_csv(data_path)

# Set page title
st.title("Interactive Food Nutrient Explorer")

# Sidebar for navigation
st.sidebar.header("Options")
view_data = st.sidebar.checkbox("Show Raw Data")
nutrient_to_visualize = st.sidebar.selectbox(
    "Select Nutrient to Visualize",
    ['energy_kcal', 'protein', 'total_fat', 'dietary_fiber',
     'carbohydrate', 'iron_(fe)', 'calcium_(ca)', 'zinc_(zn)',
     'magnesium_(mg)', 'phosphorus_(p)', 'potassium_(k)', 'sodium_(na)']
)

# Display dataset if selected
if view_data:
    st.subheader("Dataset Overview")
    st.write(food_data)

# Nutrient Distribution Visualization
st.header("Nutrient Distribution Across Food Groups")
st.write(f"Visualizing: **{nutrient_to_visualize.replace('_', ' ').capitalize()}**")

# Generate the bar plot for nutrient distribution
fig, ax = plt.subplots(figsize=(10, 6))
food_data.groupby('food_group')[nutrient_to_visualize].mean().sort_values().plot(
    kind='bar', ax=ax, title=f'Average {nutrient_to_visualize.replace("_", " ").capitalize()} by Food Group'
)
ax.set_ylabel(f'Average {nutrient_to_visualize.replace("_", " ").capitalize()}')
ax.set_xlabel('Food Group')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig)

# Correlation Heatmap
st.header("Nutrient Correlation Heatmap")
correlation = food_data.select_dtypes(include=['float64', 'int64']).corr()
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
ax.set_title('Correlation Heatmap of Nutrients')
st.pyplot(fig)

# Search Functionality
st.header("Search Food Items")
search_query = st.text_input("Enter food name or group:")
if search_query:
    search_results = food_data[
        food_data['food_name'].str.contains(search_query, case=False, na=False) |
        food_data['food_group'].str.contains(search_query, case=False, na=False)
    ]
    st.write("Search Results:", search_results)

# Footer
st.sidebar.info("Developed using Streamlit")
