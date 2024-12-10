import streamlit as st
import pandas as pd
import plotly.express as px

# App title
st.title("Medical Education and Healthcare Data Analysis")
st.write("Analyze the current state of medical education seats and doctor statistics in India.")

# Load data
data = {
    "Category": [
        "MBBS Seats (Total)",
        "MBBS Seats (Government)",
        "MBBS Seats (Private)",
        "PG Seats (MD/MS)",
        "Super-Speciality Seats (DM/MCh)",
        "Super-Speciality Seats (Government)",
        "Super-Speciality Seats (Private)",
        "DNB/FNB Seats (Total)",
        "CPS Seats (Diploma and Fellowship)",
        "Registered Allopathic Doctors (Total)",
        "Actively Practicing Doctors (Estimated)",
        "Doctor-Population Ratio",
        "Medical Colleges Growth (2014-2024)",
        "MBBS Seats Growth (2014-2024)",
        "PG Seats Growth (2014-2024)",
        "Projected MBBS Seats Increase (Next 10 Years)"
    ],
    "Seats": [
        118137,
        60422,
        57715,
        73157,
        4997,
        3909,
        1088,
        13246,
        1621,
        1308009,
        1046407,
        "1:834",
        "387 to 780 (102% Increase)",
        "51,348 to 118,137 (130% Increase)",
        "Unknown, but PG seats have grown significantly",
        "+75,000 (Projected)"
    ]
}

df = pd.DataFrame(data)

# Separate numeric and textual data
df_numeric = df[df["Seats"].apply(lambda x: str(x).replace(",", "").isdigit())].copy()
df_numeric["Seats"] = df_numeric["Seats"].astype(int)
df_textual = df[~df.index.isin(df_numeric.index)]

# Display the data
st.write("### Dataset Overview")
st.dataframe(df)

# Display numeric data insights
st.write("### Numeric Data Insights")
top_insights = df_numeric.nlargest(10, "Seats")
st.write(top_insights)

# Bar chart for numeric data
st.write("### Bar Chart: Top Categories by Seats")
fig1 = px.bar(top_insights, x="Category", y="Seats", title="Top Categories by Seats", text="Seats")
st.plotly_chart(fig1)

# Pie chart for numeric data
#st.write("### Pie Chart: Seats Distribution")
#fig2 = px.pie(df_numeric, names="Category", values="Seats", title="Seats Distribution")
#st.plotly_chart(fig2)

# Display textual data insights
st.write("### Textual Data Insights")
st.write("These entries provide qualitative insights or projections:")
for _, row in df_textual.iterrows():
    st.write(f"**{row['Category']}**: {row['Seats']}")

# Projected MBBS Seats Increase Visualization
st.write("### Projected MBBS Seats Increase Visualization")
projected_growth = {"Year": list(range(2024, 2034)), "MBBS Seats": []}
current_seats = 118137
growth_rate = 0.05  # Assuming 5% annual growth
for year in projected_growth["Year"]:
    current_seats += int(current_seats * growth_rate)
    projected_growth["MBBS Seats"].append(current_seats)

df_projection = pd.DataFrame(projected_growth)
fig3 = px.line(df_projection, x="Year", y="MBBS Seats", title="Projected MBBS Seats Growth (Next 10 Years)")
st.plotly_chart(fig3)

# Doctor-Population Ratio Representation
st.write("### Doctor-Population Ratio Visualization")
fig4 = px.bar(
    x=["Doctor", "Population"],
    y=[1, 834],
    title="Doctor-Population Ratio",
    labels={"x": "Category", "y": "Count"}
)
st.plotly_chart(fig4)
