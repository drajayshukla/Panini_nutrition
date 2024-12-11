import streamlit as st
import requests


# Function to validate DOI
def validate_doi(doi):
    url = f"https://api.crossref.org/works/{doi}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            container_title = data.get('message', {}).get('container-title', [])
            publisher = data.get('message', {}).get('publisher', '')

            # Check if the DOI belongs to JCEM
            is_jcem = "The Journal of Clinical Endocrinology & Metabolism" in container_title
            return is_jcem, container_title, publisher
        else:
            return None, None, None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None, None


# Streamlit App Interface
st.title("JCEM DOI Validator")
st.write("Enter a DOI to check if it belongs to **The Journal of Clinical Endocrinology & Metabolism (JCEM)**.")

# Input Field
doi = st.text_input("Enter DOI:", placeholder="e.g., 10.1210/clinem/dgae835")

if doi:
    st.write("Validating DOI...")
    is_jcem, container_title, publisher = validate_doi(doi)

    if is_jcem is None:
        st.error("DOI could not be validated. Please check the DOI or try again later.")
    elif is_jcem:
        st.success(f"✅ The DOI belongs to **JCEM**!")
        st.write(f"**Journal Title:** {container_title[0] if container_title else 'N/A'}")
        st.write(f"**Publisher:** {publisher}")
    else:
        st.error(f"❌ The DOI does not belong to JCEM.")
        st.write(f"**Journal Title:** {container_title[0] if container_title else 'N/A'}")
        st.write(f"**Publisher:** {publisher if publisher else 'N/A'}")

st.write("Powered by [CrossRef API](https://www.crossref.org/) and Streamlit.")
