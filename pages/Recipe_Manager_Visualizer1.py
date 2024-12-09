import streamlit as st
import pandas as pd
import os

# Function to load data from selected files
@st.cache_data
def load_data(file_list):
    # Combine all selected CSV files into one DataFrame
    data = pd.concat([pd.read_csv(file) for file in file_list], ignore_index=True)
    return data

# Function to get all file paths
def get_file_paths():
    file_paths = [f"data/recipechunk_{i}.csv" for i in range(1, 36)]
    return file_paths

# App title
st.title("Recipe Explorer")

# Sidebar - File Selection
st.sidebar.header("Select Files")
file_options = ["All"] + [f"recipechunk_{i}.csv" for i in range(1, 36)]
selected_files = st.sidebar.multiselect("Choose files to load:", file_options, default="recipechunk_2")

# Determine files to load
file_paths = get_file_paths()
if "All" in selected_files:
    selected_file_paths = file_paths
else:
    selected_file_paths = [f"data/{file}" for file in selected_files]

# Load data
if selected_file_paths:
    data = load_data(selected_file_paths)

    # Sidebar filters
    st.sidebar.header("Filter Recipes")

    # Cuisine filter
    cuisines = st.sidebar.multiselect(
        "Select Cuisine(s)",
        options=data['Cuisine'].unique(),
        default=data['Cuisine'].unique()
    )

    # Course filter
    courses = st.sidebar.multiselect(
        "Select Course(s)",
        options=data['Course'].unique(),
        default=data['Course'].unique()
    )

    # Diet filter
    diets = st.sidebar.multiselect(
        "Select Diet(s)",
        options=data['Diet'].unique(),
        default=data['Diet'].unique()
    )

    # Filter data
    filtered_data = data[
        (data['Cuisine'].isin(cuisines)) &
        (data['Course'].isin(courses)) &
        (data['Diet'].isin(diets))
    ]

    # Display filtered recipes
    st.subheader(f"Showing {len(filtered_data)} Recipes")
    for index, row in filtered_data.iterrows():
        with st.expander(f"{row['RecipeName']}"):
            st.markdown(f"**Cuisine**: {row['Cuisine']}")
            st.markdown(f"**Course**: {row['Course']}")
            st.markdown(f"**Diet**: {row['Diet']}")
            st.markdown(f"**Prep Time**: {row['PrepTimeInMins']} mins")
            st.markdown(f"**Cook Time**: {row['CookTimeInMins']} mins")
            st.markdown(f"**Total Time**: {row['TotalTimeInMins']} mins")
            st.markdown(f"**Servings**: {row['Servings']}")
            st.markdown(f"**Ingredients**: {row['Ingredients']}")
            st.markdown(f"**Instructions**: {row['Instructions']}")
            if pd.notnull(row['URL']):
                st.markdown(f"[View Full Recipe]({row['URL']})")

    # Search bar
    st.sidebar.subheader("Search Recipes")
    search_term = st.sidebar.text_input("Search by Recipe Name")

    if search_term:
        search_results = data[data['RecipeName'].str.contains(search_term, case=False, na=False)]
        st.subheader(f"Search Results for '{search_term}': {len(search_results)} Recipes Found")
        for index, row in search_results.iterrows():
            with st.expander(f"{row['RecipeName']}"):
                st.markdown(f"**Cuisine**: {row['Cuisine']}")
                st.markdown(f"**Course**: {row['Course']}")
                st.markdown(f"**Diet**: {row['Diet']}")
                st.markdown(f"**Prep Time**: {row['PrepTimeInMins']} mins")
                st.markdown(f"**Cook Time**: {row['CookTimeInMins']} mins")
                st.markdown(f"**Total Time**: {row['TotalTimeInMins']} mins")
                st.markdown(f"**Servings**: {row['Servings']}")
                st.markdown(f"**Ingredients**: {row['Ingredients']}")
                st.markdown(f"**Instructions**: {row['Instructions']}")
                if pd.notnull(row['URL']):
                    st.markdown(f"[View Full Recipe]({row['URL']})")

    # Visualization
    st.sidebar.subheader("Visualize Recipes")
    if st.sidebar.checkbox("Show Cuisine Distribution"):
        st.subheader("Cuisine Distribution")
        cuisine_counts = data['Cuisine'].value_counts()
        st.bar_chart(cuisine_counts)

    if st.sidebar.checkbox("Show Course Distribution"):
        st.subheader("Course Distribution")
        course_counts = data['Course'].value_counts()
        st.bar_chart(course_counts)
else:
    st.warning("Please select at least one file to load data.")
