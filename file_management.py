import os
from pathlib import Path
import streamlit as st

# Path for storing PDFs
PDF_FOLDER = Path("pdf_storage")
os.makedirs(PDF_FOLDER, exist_ok=True)


def list_pdfs():
    """
    List all PDF files in the PDF folder.
    Returns:
        list: List of PDF file names.
    """
    return [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]


def upload_pdf(uploaded_file):
    """
    Save an uploaded PDF file to the storage directory.
    Args:
        uploaded_file: The uploaded file object from Streamlit.
    Returns:
        str: Path to the saved PDF file.
    """
    if uploaded_file:
        file_path = PDF_FOLDER / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None


def delete_pdf(file_name):
    """
    Delete a PDF file from the storage directory.
    Args:
        file_name (str): The name of the file to delete.
    """
    file_path = PDF_FOLDER / file_name
    if file_path.exists():
        os.remove(file_path)
        st.success(f"{file_name} has been deleted.")
    else:
        st.error(f"{file_name} does not exist.")


def download_pdf(file_name):
    """
    Provide a PDF file for download in Streamlit.
    Args:
        file_name (str): The name of the file to download.
    """
    file_path = PDF_FOLDER / file_name
    if file_path.exists():
        with open(file_path, "rb") as f:
            st.download_button(label="Download", data=f, file_name=file_name)
    else:
        st.error(f"{file_name} does not exist.")
