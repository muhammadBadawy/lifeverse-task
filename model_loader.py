import os
import requests
import torch
from torchvision import models
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def download_file(url, file_path):
    """Downloads a file from a URL to the given file path."""
    if not os.path.exists(file_path):
        print(f"Downloading {file_path}...")
        response = requests.get(url)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {file_path}.")
    else:
        print(f"{file_path} already exists.")

def download_model_and_labels(model_name, model_url, label_url, model_dir):
    """Downloads the model and labels from external sources if not already present."""
    model_folder = os.path.join(model_dir, model_name)
    model_path = os.path.join(model_folder, f"{model_name}.pth")
    label_path = os.path.join(model_folder, "imagenet_classes.txt")

    os.makedirs(model_folder, exist_ok=True)

    # Download the model and the labels
    download_file(model_url, model_path)
    download_file(label_url, label_path)

    return model_path, label_path

def load_model(model_name, model_path):
    """Loads the specified pre-trained model."""
    if model_name == "resnet18":
        model = models.resnet18()
    else:
        raise ValueError(f"Model {model_name} is not supported")

    # Load the downloaded state dictionary
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

    # Set the model to evaluation mode
    model.eval()
    return model

def load_labels(label_path):
    """Loads the labels for the model."""
    with open(label_path) as f:
        labels = [line.strip() for line in f.readlines()]
    return labels

# Main function to handle model download and loading
def initialize_model():
    model_name = os.getenv("MODEL_NAME")
    model_url = os.getenv("MODEL_URL")
    label_url = os.getenv("LABEL_URL")
    model_dir = os.getenv("MODEL_DIR")

    model_path, label_path = download_model_and_labels(model_name, model_url, label_url, model_dir)
    model = load_model(model_name, model_path)
    labels = load_labels(label_path)

    return model, labels
