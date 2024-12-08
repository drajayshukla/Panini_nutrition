import streamlit as st
import pandas as pd

# Load the CSV file
@st.cache
def load_data(filepath):
    data = pd.read_csv(filepath)
    return data

# Load your dataset
csv_file = "data/index.csv"  # Adjust path as necessary
df = load_data(csv_file)

# Ensure numeric columns are properly converted
numeric_cols = [col for col in df.columns if "e" in col.lower() or "Energy" in col or "Protein" in col]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Streamlit App
st.title("Food Nutritional Details")
st.write("Search and explore detailed information about food items.")

# Search options
st.sidebar.header("Search Options")
search_by = st.sidebar.radio(
    "Search by:",
    options=["Food Code", "Food Name", "Local Name"],
    index=0
)

search_query = st.sidebar.text_input(f"Enter {search_by} to search:")

# Nutritional categories to display
st.sidebar.header("Select Nutritional Details")
default_selection = ["Energy; enerc", "Protein; protcnt"]
nutritional_columns = [col for col in df.columns if col not in ["Food Code", "Food Name", "Scientific Name", "Local Name", "Food Group", "Tags"]]
selected_columns = st.sidebar.multiselect(
    "Select nutritional details to display:",
    options=nutritional_columns,
    default=default_selection
)

# Filter the dataset based on the search query
filtered_df = pd.DataFrame()
if search_query:
    if search_by == "Food Code":
        filtered_df = df[df["Food Code; code"].str.contains(search_query, case=False, na=False)]
    elif search_by == "Food Name":
        filtered_df = df[df["Food Name; name"].str.contains(search_query, case=False, na=False)]
    elif search_by == "Local Name":
        filtered_df = df[df["Local Name; lang"].str.contains(search_query, case=False, na=False)]

# Display results
if not filtered_df.empty:
    st.subheader("Search Results")
    for index, row in filtered_df.iterrows():
        st.write(f"### {row['Food Name; name']}")
        st.write(f"**Food Code:** {row['Food Code; code']}")
        st.write(f"**Scientific Name:** {row['Scientific Name; scie']}")
        st.write(f"**Local Name:** {row['Local Name; lang']}")
        st.write(f"**Food Group:** {row['Food Group; grup']}")
        st.write(f"**Tags:** {row['Tags; tags']}")
        st.write("---")

        # Display selected nutritional details
        st.write("#### Nutritional Details")
        for col in selected_columns:
            st.write(f"**{col.split(';')[0]}:** {row[col]}")

        st.markdown("---")
else:
    st.warning("No results found. Please refine your search.")

