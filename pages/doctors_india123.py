import streamlit as st
import pandas as pd
import plotly.express as px

# App title
st.title("Medical Education and Healthcare Data Analysis")
st.write("Analyze the current state of medical education seats and doctor statistics in India.")

# Load data
data = {
    "Category": [
        "MBBS Seats_all/year",
        "MBBS Seats (Government)/year",
        "MBBS Seats (Private)/year",
        "PG Seats (MD/MS)/year",
        "Super-Speciality Seats (DM/MCh)/year",
        "Super-Speciality Seats (Government)/year",
        "Super-Speciality Seats (Private)/year",
        "DNB/FNB Seats (Total)/year",
        "CPS Seats (Diploma and Fellowship)/year",
        "Total Registered Allopathic Doctors (Total)",
        "Actively Practicing Doctors (Total Estimated)",
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

# Display the data with references
st.write("### Dataset Overview")
st.dataframe(df)

# Display references
st.write("### References")
for index, row in df.iterrows():
    st.write(f"**{row['Category']}**: [Reference]({row['Reference']})")

# Separate numeric and textual data
df_numeric = df[df["Seats"].apply(lambda x: str(x).replace(",", "").isdigit())].copy()
df_numeric["Seats"] = df_numeric["Seats"].astype(int)
df_textual = df[~df.index.isin(df_numeric.index)]

# Display numeric insights
st.write("### Numeric Data Insights")
top_insights = df_numeric.nlargest(10, "Seats")
st.write(top_insights)

# Bar chart for numeric data
st.write("### Bar Chart: Top Categories by Seats")
fig1 = px.bar(top_insights, x="Category", y="Seats", title="Top Categories by Seats", text="Seats")
st.plotly_chart(fig1)

# Textual data insights
st.write("### Textual Data Insights")
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
fig2 = px.line(df_projection, x="Year", y="MBBS Seats", title="Projected MBBS Seats Growth (Next 10 Years)")
st.plotly_chart(fig2)
