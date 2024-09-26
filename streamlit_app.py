import streamlit as st
from PIL import Image
import torch
from torchvision import models, transforms
import os
import requests
from model_loader import initialize_model

model, labels = initialize_model()

# Define the image transformation
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def classify_image(image: Image.Image):
    """Classifies the given image using the pre-trained ResNet model."""
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Apply transformations
    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension

    # Run the model and get predictions
    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = outputs.max(1)
        predicted_class = labels[predicted.item()]

    return predicted_class

# Streamlit interface
st.title("Image Classification with ResNet")
st.write("Upload an image to classify it using a pre-trained ResNet model.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)

    # Display the image
    st.image(image, caption='Uploaded Image', use_column_width=True)

    st.write("Classifying...")

    # Get the prediction
    predicted_class = classify_image(image)

    # Display the prediction
    st.write(f"Prediction: **{predicted_class}**")
