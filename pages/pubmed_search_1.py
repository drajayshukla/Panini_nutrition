import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlencode

# PubMed API Base URL
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/esummary.fcgi"

# NCBI API Key (optional for higher rate limits)
API_KEY = None  # Replace with your API Key if available

# Fetch PMIDs from PubMed
def fetch_pmids(journal, start_year, end_year, num_articles):
    query = f'"{journal}"[jour] AND ("{start_year}/01/01"[Date - Publication] : "{end_year}/12/31"[Date - Publication])'
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": num_articles,
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
    This app retrieves articles from PubMed for selected journals, filtered by year range and number of articles.
    """)

    # Sidebar Filters
    st.sidebar.header("Filters")
    journal = st.sidebar.selectbox("Select Journal", ["N Engl J Med", "The Lancet", "Nature"])
    start_year = st.sidebar.number_input("Start Year", min_value=1900, max_value=2023, value=2010)
    end_year = st.sidebar.number_input("End Year", min_value=1900, max_value=2023, value=2023)
    num_articles = st.sidebar.number_input("Number of Articles", min_value=1, max_value=500, value=100)

    if st.sidebar.button("Fetch Articles"):
        with st.spinner("Fetching articles..."):
            # Fetch PMIDs
            pmids = fetch_pmids(journal, start_year, end_year, num_articles)
            if pmids:
                # Fetch Article Details
                articles = fetch_article_details(pmids)
                if articles:
                    st.success(f"Fetched {len(articles)} articles!")
                    df = pd.DataFrame(articles)

                    # Display DataFrame
                    st.dataframe(df)

                    # Generate Clickable Links in CSV
                    csv_data = df.to_csv(index=False).encode("utf-8")
                    csv_data_clickable = df.copy()
                    csv_data_clickable["Link"] = csv_data_clickable["Link"].apply(lambda x: f'=HYPERLINK("{x}", "{x}")')

                    st.download_button(
                        label="Download Clickable CSV",
                        data=csv_data_clickable.to_csv(index=False, sep=",", quotechar='"'),
                        file_name=f"{journal}_articles_{start_year}_{end_year}.csv",
                        mime="text/csv",
                    )
                else:
                    st.warning("No articles found.")
            else:
                st.warning("No PMIDs found for the given criteria.")

if __name__ == "__main__":
    main()
