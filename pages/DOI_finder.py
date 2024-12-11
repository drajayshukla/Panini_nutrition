import requests

def validate_doi(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Check if the journal title matches JCEM
        if "The Journal of Clinical Endocrinology & Metabolism" in data.get('message', {}).get('container-title', []):
            return True
    return False

# Example usage
doi = "10.1210/clinem/dgae286"
is_jcem = validate_doi(doi)
print("Is JCEM DOI?", is_jcem)
