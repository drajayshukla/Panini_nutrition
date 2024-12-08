import json
from pathlib import Path

# Path to favorites file
FAVORITES_FILE = Path("data/favorites.json")

# Load favorite pages
def load_favorites():
    """
    Load favorite pages from the JSON file.
    Returns:
        list: A list of favorite page names.
    """
    if FAVORITES_FILE.exists():
        with open(FAVORITES_FILE, "r") as file:
            return json.load(file).get("favorites", [])
    return []

# Save favorite pages
def save_favorites(favorites):
    """
    Save favorite pages to the JSON file.
    Args:
        favorites (list): List of favorite page names to save.
    """
    with open(FAVORITES_FILE, "w") as file:
        json.dump({"favorites": favorites}, file)

# Check if a page is in favorites
def is_favorite(page_name):
    """
    Check if a page is marked as a favorite.
    Args:
        page_name (str): Name of the page to check.
    Returns:
        bool: True if the page is a favorite, False otherwise.
    """
    favorites = load_favorites()
    return page_name in favorites

# Toggle favorite status
def toggle_favorite(page_name):
    """
    Toggle the favorite status of a page.
    Args:
        page_name (str): Name of the page to toggle.
    Returns:
        list: Updated list of favorite pages.
    """
    favorites = load_favorites()
    if page_name in favorites:
        favorites.remove(page_name)
    else:
        favorites.append(page_name)
    save_favorites(favorites)
    return favorites
