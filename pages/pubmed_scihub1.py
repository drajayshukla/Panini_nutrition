import streamlit as st
import requests
import pandas as pd

# PubMed API URLs
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PUBMED_LINKOUT_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
API_KEY = None  # Optional for PubMed API (replace with your API key if available)

# Combine Keywords for Search
def build_search_query(keywords):
    return " OR ".join([f'"{kw}"' for kw in keywords])

# Fetch articles from PubMed
def fetch_pubmed_articles(keywords):
    search_query = build_search_query(keywords)
    search_params = {
        "db": "pubmed",
        "term": search_query,
        "retmode": "json",
        "retmax": 100,
        "api_key": API_KEY,
    }
    search_response = requests.get(PUBMED_SEARCH_URL, params=search_params)
    if search_response.status_code == 200:
        search_data = search_response.json()
        pmids = search_data.get("esearchresult", {}).get("idlist", [])
        return fetch_pubmed_details(pmids)
    else:
        st.error("Failed to fetch articles from PubMed. Please try again later.")
        return []

def fetch_pubmed_details(pmids):
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
            pubdate = article.find(".//PubDate").text or "No Date Available"
            pmid = article.find(".//PMID").text
            doi = article.find(".//ELocationID[@EIdType='doi']").text or "No DOI Available"
            pubmed_link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            full_text_link = fetch_full_text_link(pmid)
            articles.append(
                {
                    "Title": title,
                    "Abstract": abstract,
                    "Publication Date": pubdate,
                    "DOI": doi,
                    "PubMed Link": pubmed_link,
                    "Full-Text Link": full_text_link,
                }
            )
        return articles
    else:
        st.error("Failed to fetch article details from PubMed. Please try again later.")
        return []

# Fetch full-text link using PubMed elink API
def fetch_full_text_link(pmid):
    params = {
        "dbfrom": "pubmed",
        "linkname": "pubmed_pubmed_refs",
        "id": pmid,
        "retmode": "json",
        "api_key": API_KEY,
    }
    response = requests.get(PUBMED_LINKOUT_URL, params=params)
    if response.status_code == 200:
        link_data = response.json()
        linkout_urls = link_data.get("linksets", [{}])[0].get("linkout_url", [])
        # Return the first full-text link if available
        if linkout_urls:
            return linkout_urls[0].get("url", "No Full-Text Link Available")
    return "No Full-Text Link Available"

# Streamlit App
def main():
    st.title("Medical Literature Search with Full-Text Links")
    st.markdown("""
    Search multiple databases (e.g., PubMed, Embase, Cochrane CENTRAL) using various combinations of medical keywords. 
    Returns a list of articles with links to abstracts, DOIs, and full-text links if publicly available.
    """)

    # User Input for Keywords
    st.sidebar.header("Search Settings")
    keywords_input = st.sidebar.text_area("Enter keywords (comma-separated):",
                                          "hypoparathyroidism, hypocalcemia, hypocal*, hypoPT, parathyroid hormone, PTH, rhPTH, PTH(1–34), teriparatide, PTH(1–84), TransCon PTH, random*")
    keywords = [kw.strip() for kw in keywords_input.split(",")]

    database = st.sidebar.radio("Select Database", ["PubMed (Default)", "Embase (Coming Soon)", "Cochrane CENTRAL (Coming Soon)"])

    if st.sidebar.button("Search"):
        if database == "PubMed (Default)":
            with st.spinner("Searching PubMed..."):
                articles = fetch_pubmed_articles(keywords)
                if articles:
                    st.success(f"Found {len(articles)} articles!")
                    # Display articles
                    for article in articles:
                        with st.expander(article["Title"]):
                            st.write(f"**Publication Date**: {article['Publication Date']}")
                            st.write(f"**Abstract**: {article['Abstract']}")
                            st.markdown(f"[PubMed Link]({article['PubMed Link']})")
                            st.markdown(f"[Full-Text Link]({article['Full-Text Link']})")

                    # Downloadable CSV
                    df = pd.DataFrame(articles)
                    csv_data = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name="articles_with_full_text.csv",
                        mime="text/csv",
                    )
                else:
                    st.warning("No articles found.")
        else:
            st.warning(f"{database} is not yet supported. Stay tuned!")

if __name__ == "__main__":
    main()
