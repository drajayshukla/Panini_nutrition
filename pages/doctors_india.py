import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# Display the data
st.write("### Dataset Overview")
st.dataframe(df)

# Clean numeric data for analysis
df_numeric = df[df["Seats"].apply(lambda x: str(x).replace(",", "").isdigit())]
df_numeric["Seats"] = df_numeric["Seats"].apply(lambda x: int(str(x).replace(",", "")))

# Insights (Top 10 features)
st.write("### Top 10 Insights")
top_insights = df_numeric.nlargest(10, "Seats")
st.write(top_insights)

# Visualizations
st.write("### Visualizations")

# 1. Bar Chart of Top Categories by Seats
fig1 = px.bar(top_insights, x="Category", y="Seats", title="Top Categories by Seats", text="Seats")
st.plotly_chart(fig1)

# 2. Pie Chart of Seats Distribution
#fig2 = px.pie(df_numeric, names="Category", values="Seats", title="Seats Distribution")
#st.plotly_chart(fig2)

# 3. Scatter Plot of Numeric Categories
fig3 = px.scatter(df_numeric, x="Category", y="Seats", title="Scatter Plot of Seats")
st.plotly_chart(fig3)

# 4. Heatmap (Correlation not applicable; here, size comparison)
#fig4, ax = plt.subplots(figsize=(10, 6))
#sns.barplot(x="Seats", y="Category", data=top_insights, palette="coolwarm", ax=ax)
#ax.set_title("Seats Comparison (Top 10 Categories)")
#st.pyplot(fig4)

# 5. Word Cloud of Categories
#from wordcloud import WordCloud
#wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(df["Category"]))
#fig5, ax = plt.subplots(figsize=(10, 5))
#ax.imshow(wordcloud, interpolation="bilinear")
#ax.axis("off")
#st.pyplot(fig5)
