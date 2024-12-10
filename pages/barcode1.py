import streamlit as st
import requests
import numpy as np
from PIL import Image
from pyzbar.pyzbar import decode

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

# Function to decode barcode from image
def decode_barcode_image(image):
    decoded_objects = decode(image)
    if decoded_objects:
        # Return the first decoded barcode value
        return decoded_objects[0].data.decode("utf-8")
    else:
        return None  # No barcode found

# Main Function
def main():
    st.title("Food Barcode Scanner")
    st.markdown("""
    Use this tool to scan food barcodes and fetch nutritional information.  
    Data is sourced from **OpenFoodFacts**, a free and open database of food products.
    """)

    # Input barcode manually
    st.markdown("### Manual Barcode Input")
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

    # Upload barcode image
    st.markdown("### Barcode Image Upload")
    uploaded_file = st.file_uploader("Upload a Barcode Image (jpg, png, jpeg)", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Barcode Image", use_column_width=True)

            # Decode the barcode
            barcode = decode_barcode_image(image)
            if barcode:
                st.success(f"Barcode Detected: {barcode}")
                food_details = fetch_food_details(barcode)
                if food_details:
                    st.success("Product Found!")
                    st.json(food_details)
                else:
                    st.error("Product not found in the database.")
            else:
                st.error("No barcode detected in the image. Please try another image.")
        except Exception as e:
            st.error(f"An error occurred while processing the image: {e}")

if __name__ == "__main__":
    main()
