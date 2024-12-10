import streamlit as st
import torch
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Load YOLOv5 model
@st.cache_resource
def load_model():
    # Replace with your YOLOv5 model path
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
    return model

# Function to estimate calories
def estimate_calories(predictions):
    # Example calorie mapping per food class (calories per gram)
    calorie_mapping = {
        "roti": 50, "rice": 130, "dal": 80, "paneer": 300, "samosa": 150, "idli": 40, "dosa": 100,
        # Add all 36 classes with approximate values
    }
    calorie_estimation = 0
    for pred in predictions:
        class_name = pred['name']
        if class_name in calorie_mapping:
            calorie_estimation += calorie_mapping[class_name] * (pred['area'] / 10000)  # Example scaling factor
    return calorie_estimation

# Function to plot image with bounding boxes
def plot_detections(image, detections):
    for det in detections:
        xmin, ymin, xmax, ymax, confidence, cls = det[:6]
        class_name = det[-1]
        color = (0, 255, 0)
        cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
        cv2.putText(image, class_name, (int(xmin), int(ymin - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return image

# Streamlit App Layout
st.title("Indian Food Image Localization & Calorie Estimation")
st.sidebar.title("Options")

model = load_model()

# Upload Image
uploaded_file = st.sidebar.file_uploader("Upload an image of food", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    # Inference
    results = model(image_np)
    detections = results.xyxy[0].cpu().numpy()  # Extract detections
    predictions = [{"name": results.names[int(det[5])], "area": (det[2] - det[0]) * (det[3] - det[1])} for det in detections]

    # Display Detections
    st.header("Localized Food Items")
    for pred in predictions:
        st.write(f"Class: {pred['name']}, Area: {pred['area']:.2f}")

    # Calorie Estimation
    total_calories = estimate_calories(predictions)
    st.header(f"Estimated Total Calories: {total_calories:.2f} kcal")

    # Visualize Detections
    localized_image = plot_detections(image_np.copy(), detections)
    st.image(localized_image, caption="Localized Image", use_column_width=True)
else:
    st.sidebar.info("Upload an image to start.")

