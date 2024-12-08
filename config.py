import os
from pathlib import Path

# App Configuration
APP_TITLE = "Streamlit Multi-Page App"
SESSION_TIMEOUT_MINUTES = 60  # Inactivity timeout in minutes

# User credentials (Use a database or environment variables in production)
USER_CREDENTIALS = {
    "dev": "aanand",
    "raj": "kumar"
}

# Paths for directories and files
BASE_DIR = Path(__file__).resolve().parent
PAGES_DIR = BASE_DIR / "pages"  # Directory containing page scripts
PDF_FOLDER = BASE_DIR / "pdf_storage"  # Directory for storing PDFs
FAVORITES_FILE = BASE_DIR / "data" / "favorites.json"

# Ensure necessary directories exist
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(FAVORITES_FILE.parent, exist_ok=True)
