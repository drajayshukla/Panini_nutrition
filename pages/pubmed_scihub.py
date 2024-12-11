import streamlit as st
import requests
import pandas as pd

# PubMed API Base URLs
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# NCBI API Key (optional for higher rate limits)
API_KEY = None  # Replace with your API Key if available

# Journal Options
CLINICAL_JOURNALS = [
    "N Engl J Med",
    "Lancet",
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

# Fetch article details including DOI, abstracts, and Sci-Hub links using PMIDs
def fetch_article_details(pmids):
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "rettype": "abstract",
        "retmode": "xml",
        "api_key": API_KEY,
    }
    response = requests.get(PUBMED_DETAILS_URL, params=params)
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
            sci_hub_link = f"https://sci-hub.se/{doi}" if "10." in doi else "No Sci-Hub Link Available"
            articles.append(
                {
                    "Title": title,
                    "Abstract": abstract,
                    "Publication Date": pubdate,
                    "DOI": doi,
                    "PubMed Link": pubmed_link,
                    "Sci-Hub Link": sci_hub_link,
                }
            )
        return articles
    else:
        st.error("Failed to fetch article details from PubMed. Please try again later.")
        return []

# Streamlit App
def main():
    st.title("PubMed Article Finder with Abstracts, DOIs, and Sci-Hub Links")
    st.markdown("""
    This app retrieves the latest articles from PubMed for selected clinical or endocrinology journals, including abstracts, DOIs, and Sci-Hub links.
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

                    # Display abstracts in an expandable format
                    for i, row in df.iterrows():
                        with st.expander(f"{row['Title']} (Published: {row['Publication Date']})"):
                            st.write(f"**DOI**: {row['DOI']}")
                            st.write(f"**PubMed Link**: [Link]({row['PubMed Link']})")
                            st.write(f"**Sci-Hub Link**: [Link]({row['Sci-Hub Link']})")
                            st.write("**Abstract**:")
                            st.write(row["Abstract"])

                    # Prepare a downloadable CSV with abstracts
                    csv_data = pd.DataFrame(articles)  # Includes abstracts
                    csv_data = csv_data.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="Download CSV with Abstracts and Links",
                        data=csv_data,
                        file_name=f"{journal}_articles_{start_index}_to_{end_index}.csv",
                        mime="text/csv",
                    )
                else:
                    st.warning("No articles found.")

if __name__ == "__main__":
    main()
