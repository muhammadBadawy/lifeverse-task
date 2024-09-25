from flask import Flask, request, jsonify
from PIL import Image
import torch
from torchvision import models, transforms
from model_loader import initialize_model

app = Flask(__name__)

model, labels = initialize_model()

# Define the image transformation
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load ImageNet labels for classification
with open("imagenet_classes.txt") as f:
    labels = [line.strip() for line in f.readlines()]

@app.route('/classify', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Open the image file
        image = Image.open(file)

        # Convert RGBA images to RGB
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Apply transformations
        image = transform(image).unsqueeze(0)  # Add batch dimension
        with torch.no_grad():
            outputs = model(image)
            _, predicted = outputs.max(1)
            predicted_class = labels[predicted.item()]
        
        return jsonify({"class": predicted_class})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
