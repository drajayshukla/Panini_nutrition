import streamlit as st
import requests
import pandas as pd

# PubMed API Base URL
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

# NCBI API Key (optional for higher rate limits)
API_KEY = None  # Replace with your API Key if available

# Journal Options
CLINICAL_JOURNALS = [
    "N Engl J Med",
    "The Lancet",
    "JAMA",
    "BMJ",
    "Ann Intern Med",
    "PLOS Medicine",
    "J Clin Invest",
    "JAMA Intern Med",
    "Am J Med",
    "CMAJ"
]

ENDOCRINOLOGY_JOURNALS = [
    "J Clin Endocrinol Metab",
    "Diabetes Care",
    "Endocrinology",
    "Diabetologia",
    "Lancet Diabetes Endocrinol",
    "Thyroid",
    "Endocrine Reviews",
    "Bone",
    "Horm Metab Res",
    "Nature Rev Endocrinol"
]

# Fetch PMIDs from PubMed
def fetch_pmids(journal, start, end):
    params = {
        "db": "pubmed",
        "term": f'"{journal}"[jour]',
        "retstart": start,
        "retmax": end - start,
        "retmode": "json",
        "sort": "pub+date",
        "api_key": API_KEY,
    }
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    else:
        st.error("Failed to fetch PMIDs from PubMed. Please try again later.")
        return []

# Fetch article details using PMIDs
def fetch_article_details(pmids):
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json",
        "api_key": API_KEY,
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = []
        for uid, details in data.get("result", {}).items():
            if uid != "uids":  # Skip metadata key
                title = details.get("title", "No Title Available")
                pubdate = details.get("pubdate", "No Date Available")
                link = f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"
                articles.append({"Title": title, "Publication Date": pubdate, "Link": link})
        return articles
    else:
        st.error("Failed to fetch article details from PubMed. Please try again later.")
        return []

# Streamlit App
def main():
    st.title("PubMed Article Finder")
    st.markdown("""
    This app retrieves the latest articles from PubMed for selected clinical or endocrinology journals.
    """)

    # Sidebar Filters
    st.sidebar.header("Filters")
    category = st.sidebar.radio("Select Journal Category", ["Clinical Journals", "Endocrinology Journals"])
    journal_list = CLINICAL_JOURNALS if category == "Clinical Journals" else ENDOCRINOLOGY_JOURNALS
    journal = st.sidebar.selectbox("Select Journal", journal_list)
    start_index = st.sidebar.number_input("Start Index (e.g., 0)", min_value=0, value=0, step=1)
    end_index = st.sidebar.number_input("End Index (e.g., 100)", min_value=1, value=100, step=1)

    if end_index <= start_index:
        st.sidebar.error("End Index must be greater than Start Index.")

    if st.sidebar.button("Fetch Articles"):
        with st.spinner("Fetching articles..."):
            pmids = fetch_pmids(journal, start_index, end_index)
            if pmids:
                articles = fetch_article_details(pmids)
                if articles:
                    st.success(f"Fetched {len(articles)} articles from {journal}!")
                    df = pd.DataFrame(articles)

                    # Make links clickable in the Streamlit DataFrame
                    df['Link'] = df['Link'].apply(
                        lambda x: f'<a href="{x}" target="_blank">PubMed Link</a>'
                    )
                    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

                    # Prepare a downloadable CSV with links
                    csv_data = pd.DataFrame(articles)  # Original DataFrame for CSV
                    csv_data = csv_data.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="Download CSV with Links",
                        data=csv_data,
                        file_name=f"{journal}_articles_{start_index}_to_{end_index}.csv",
                        mime="text/csv",
                    )
                else:
                    st.warning("No articles found.")

if __name__ == "__main__":
    main()
