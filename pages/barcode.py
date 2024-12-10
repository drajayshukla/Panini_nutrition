import streamlit as st
import requests
import json

# Function to fetch food details from OpenFoodFacts API
def fetch_food_details(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code == 200:
        product_data = response.json()
        if product_data.get("status") == 1:  # Product found
            product = product_data.get("product", {})
            details = {
                "Product Name": product.get("product_name", "N/A"),
                "Brand": product.get("brands", "N/A"),
                "Calories (kcal)": product.get("nutriments", {}).get("energy-kcal_100g", "N/A"),
                "Protein (g)": product.get("nutriments", {}).get("proteins_100g", "N/A"),
                "Fat (g)": product.get("nutriments", {}).get("fat_100g", "N/A"),
                "Carbohydrates (g)": product.get("nutriments", {}).get("carbohydrates_100g", "N/A"),
                "Fiber (g)": product.get("nutriments", {}).get("fiber_100g", "N/A"),
                "Sugars (g)": product.get("nutriments", {}).get("sugars_100g", "N/A"),
            }
            return details
        else:
            return None  # Product not found
    else:
        return None  # API error

# Main Function
def main():
    st.title("Food Barcode Scanner")
    st.markdown("""
    Use this tool to scan food barcodes and fetch nutritional information.  
    Data is sourced from **OpenFoodFacts**, a free and open database of food products.
    """)

    # Input barcode manually
    barcode = st.text_input("Enter Barcode Number:")
    if st.button("Fetch Food Details"):
        if barcode:
            food_details = fetch_food_details(barcode)
            if food_details:
                st.success("Product Found!")
                st.json(food_details)
            else:
                st.error("Product not found. Please try another barcode.")
        else:
            st.warning("Please enter a valid barcode.")

    # Upload barcode image (Future Enhancement)
    #st.markdown("### Barcode Image (Optional)")
    #st.markdown("*This feature requires a barcode recognition API or library.*")

    #uploaded_file = st.file_uploader("Upload a Barcode Image (Optional)", type=["jpg", "jpeg", "png"])
   # if uploaded_file:
        #st.error("Barcode image scanning is currently unavailable. Please enter the barcode manually.")

if __name__ == "__main__":
    main()
