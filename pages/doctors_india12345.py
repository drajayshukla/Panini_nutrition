import streamlit as st
import pandas as pd
import plotly.express as px

# App title
st.title("Medical Education and Healthcare Data Analysis")
st.write("Analyze the current state of medical education seats and doctor statistics in India.")

# Load data
data = {
    "Category": [
        "MBBS Seats/year (All)",
        "MBBS Seats/year (Government)",
        "MBBS Seats/year (Private)",
        "PG Seats/year (MD/MS)",
        "Super-Speciality Seats/year (DM/MCh)",
        "Super-Speciality Seats/year (Government)",
        "Super-Speciality Seats/year (Private)",
        "DNB/FNB Seats/year (Total)",
        "CPS Seats/year (Diploma and Fellowship)",
        "Total Registered Allopathic Doctors",
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
    ],
    "Reference": [
        "https://medicaldialogues.in/news/education/medical-admissions/118137-mbbs-seats-available-in-india-maximum-seats-in-karnataka-medical-colleges-in-up-health-ministry-gives-break-up-139115",
        "https://medicaldialogues.in/news/education/medical-admissions/118137-mbbs-seats-available-in-india-maximum-seats-in-karnataka-medical-colleges-in-up-health-ministry-gives-break-up-139115",
        "https://medicaldialogues.in/news/education/medical-admissions/118137-mbbs-seats-available-in-india-maximum-seats-in-karnataka-medical-colleges-in-up-health-ministry-gives-break-up-139115",
        "https://medicaldialogues.in/news/education/medical-admissions/118137-mbbs-seats-available-in-india-maximum-seats-in-karnataka-medical-colleges-in-up-health-ministry-gives-break-up-139115",
        "https://medicaldialogues.in/news/education/101043-mbbs-45471-md-ms-pg-diploma-4997-ss-seats-available-across-660-medical-colleges-in-india-108702",
        "https://medicaldialogues.in/news/education/101043-mbbs-45471-md-ms-pg-diploma-4997-ss-seats-available-across-660-medical-colleges-in-india-108702",
        "https://medicaldialogues.in/news/education/101043-mbbs-45471-md-ms-pg-diploma-4997-ss-seats-available-across-660-medical-colleges-in-india-108702",
        "https://medicaldialogues.in/news/education/101043-mbbs-45471-md-ms-pg-diploma-4997-ss-seats-available-across-660-medical-colleges-in-india-108702",
        "https://medicaldialogues.in/news/education/101043-mbbs-45471-md-ms-pg-diploma-4997-ss-seats-available-across-660-medical-colleges-in-india-108702",
        "https://pib.gov.in/PressReleaseIframePage.aspx?PRID=1985423",
        "https://pib.gov.in/PressReleaseIframePage.aspx?PRID=1985423",
        "https://pib.gov.in/PressReleaseIframePage.aspx?PRID=1985423",
        "https://www.indiatoday.in/education-today/news/story/india-medical-colleges-numbers-double-mbbs-seats-130-percent-pg-seats-rise-135-percent-2645659-2024-12-05",
        "https://www.indiatoday.in/education-today/news/story/india-medical-colleges-numbers-double-mbbs-seats-130-percent-pg-seats-rise-135-percent-2645659-2024-12-05",
        "https://www.indiatoday.in/education-today/news/story/india-medical-colleges-numbers-double-mbbs-seats-130-percent-pg-seats-rise-135-percent-2645659-2024-12-05",
        "https://www.theweek.in/wire-updates/national/2024/10/04/bom26-gj-shah-medical-seats.html"
    ]
}

df = pd.DataFrame(data)

# Display the full dataset
st.write("### Full Dataset Overview")
st.dataframe(df, use_container_width=True, height=600)

# Separate per-year data and non-per-year data
excluded_categories = [
    "Total Registered Allopathic Doctors",
    "Actively Practicing Doctors (Estimated)",
    "Doctor-Population Ratio",
    "Medical Colleges Growth (2014-2024)",
    "MBBS Seats Growth (2014-2024)",
    "PG Seats Growth (2014-2024)",
    "Projected MBBS Seats Increase (Next 10 Years)"
]
df_per_year = df[~df["Category"].isin(excluded_categories)]
df_non_per_year = df[df["Category"].isin(excluded_categories)]

# **Section 1: Per-Year Data**
st.write("### Per-Year Data")
st.dataframe(df_per_year, use_container_width=True, height=600)

# Visualization for Per-Year Data
st.write("### Per-Year Data Visualization")
fig1 = px.bar(df_per_year, x="Category", y="Seats", title="Per-Year Data by Category", text="Seats")
st.plotly_chart(fig1)

# **Section 2: Non-Per-Year Data**
st.write("### Non-Per-Year Data")
st.dataframe(df_non_per_year, use_container_width=True, height=400)

# **Section 3: Projections**
st.write("### Projected MBBS Seats Growth for the Next 10 Years")
projected_growth = {"Year": list(range(2024, 2034)), "MBBS Seats": []}
current_seats = 118137
growth_rate = 0.05  # Assuming 5% annual growth
for year in projected_growth["Year"]:
    current_seats += int(current_seats * growth_rate)
    projected_growth["MBBS Seats"].append(current_seats)

df_projection = pd.DataFrame(projected_growth)
fig2 = px.line(df_projection, x="Year", y="MBBS Seats", title="Projected MBBS Seats Growth (Next 10 Years)")
st.plotly_chart(fig2)

# **References**
st.write("### References")
for index, row in df.iterrows():
    st.write(f"**{row['Category']}**: [Reference]({row['Reference']})")
