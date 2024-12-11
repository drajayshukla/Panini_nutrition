import streamlit as st
import requests
import pandas as pd
import urllib.parse

# PubMed API URLs
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# PubMed API Parameters
API_KEY = None  # Replace with your PubMed API Key if available

# Function to fetch PMIDs from PubMed
def fetch_pmids(query, start=0):
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 200,  # Number of results to fetch per page
        "retstart": start,  # Offset for pagination
        "sort": "date",
        "api_key": API_KEY,
    }
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        pmids = data.get("esearchresult", {}).get("idlist", [])
        total_count = int(data.get("esearchresult", {}).get("count", 0))
        return pmids, total_count
    else:
        st.error("Failed to fetch articles from PubMed.")
        return [], 0

# Function to fetch article details using PMIDs
def fetch_article_details(pmids):
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "rettype": "abstract",
        "retmode": "xml",
        "api_key": API_KEY,
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    if response.status_code == 200:
        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.content)
        articles = []
        for article in root.findall(".//PubmedArticle"):
            title = article.find(".//ArticleTitle").text or "No Title Available"
            abstract = (
                " ".join([p.text for p in article.findall(".//AbstractText") if p.text])
                or "No Abstract Available"
            )
            pubdate = article.find(".//PubDate/Year").text or "No Date Available"
            pmid = article.find(".//PMID").text
            pubmed_link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            articles.append(
                {
                    "Title": title,
                    "Abstract": abstract,
                    "Publication Date": pubdate,
                    "PubMed Link": pubmed_link,
                }
            )
        return articles
    else:
        st.error("Failed to fetch article details from PubMed.")
        return []

# Function to extract query from PubMed URL
def extract_query_from_url(url):
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    term = query_params.get("term", [None])[0]
    if term:
        return term.replace("%20", " ")
    return None

# Streamlit App
def main():
    st.title("PubMed Article Fetcher")
    st.markdown(
        """
        This app retrieves articles from PubMed based on a query or a PubMed search URL provided by the user.

        **Options:**
        1. Enter a custom query to search PubMed.
        2. Paste a PubMed search URL.

        Results are sorted by date, with support for pagination.
        """
    )

    # Input options
    query_input = st.text_area("Enter a PubMed search query:", placeholder="e.g., (hypoparathyroidism OR hypocalcemia) AND random*")
    url_input = st.text_input("Or paste a PubMed search URL:", placeholder="https://pubmed.ncbi.nlm.nih.gov/?term=(hypoparathyroidism+OR+hypocalcemia)+AND+random*")

    # Determine query from input
    query = None
    if url_input:
        query = extract_query_from_url(url_input)
        if not query:
            st.error("Invalid PubMed URL. Ensure it contains a valid 'term=' parameter.")
    elif query_input.strip():
        query = query_input.strip()

    if query:
        page = st.number_input("Select page:", min_value=1, value=1, step=1)
        if st.button("Fetch Articles"):
            with st.spinner("Fetching articles from PubMed..."):
                start = (page - 1) * 200
                pmids, total_count = fetch_pmids(query, start=start)
                if pmids:
                    articles = fetch_article_details(pmids)
                    if articles:
                        st.success(f"Found {len(articles)} articles (showing page {page} of {((total_count - 1) // 200) + 1}).")

                        # Display articles
                        for article in articles:
                            with st.expander(article["Title"]):
                                st.write(f"**Publication Date**: {article['Publication Date']}")
                                st.write(f"**Abstract**: {article['Abstract']}")
                                st.markdown(f"[PubMed Link]({article['PubMed Link']})")

                        # Prepare and download a CSV
                        df = pd.DataFrame(articles)
                        csv_data = df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            label="Download CSV",
                            data=csv_data,
                            file_name="pubmed_articles.csv",
                            mime="text/csv",
                        )
                    else:
                        st.warning("No articles found.")
    else:
        st.warning("Please provide a query or a valid PubMed search URL.")

if __name__ == "__main__":
    main()
