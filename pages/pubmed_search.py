import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlencode

# PubMed API Base URL
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

# NCBI API Key (optional for higher rate limits)
API_KEY = None  # Replace with your API Key if available

# Fetch PMIDs from PubMed
def fetch_pmids(journal, num_articles):
    params = {
        "db": "pubmed",
        "term": f'"{journal}"[jour]',
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
    st.title("NEJM Articles - PubMed Link Finder")
    st.markdown("""
    This app retrieves the latest articles from the **New England Journal of Medicine (NEJM)** on PubMed.
    """)

    # Input for number of articles to fetch
    num_articles = st.number_input(
        "Enter the number of articles to fetch (max 500):",
        min_value=1,
        max_value=500,
        value=200,
    )

    if st.button("Fetch Articles"):
        with st.spinner("Fetching articles..."):
            pmids = fetch_pmids("N Engl J Med", num_articles)
            if pmids:
                articles = fetch_article_details(pmids)
                if articles:
                    st.success(f"Fetched {len(articles)} articles!")
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
                        file_name="nejm_articles.csv",
                        mime="text/csv",
                    )
                else:
                    st.warning("No articles found.")

if __name__ == "__main__":
    main()
