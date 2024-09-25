import pytest
from PIL import Image
from streamlit_app import classify_image

@pytest.fixture
def test_image():
    """Provides a sample image for testing."""
    return Image.new('RGB', (224, 224), color='red')

def test_classify_image(test_image):
    """Tests the classification of an image."""
    # Assuming you have a way to mock or modify the output of the model
    # Since this is using a pre-trained model, the actual result will depend
    # on the image and the model output, but we are focusing on ensuring the
    # function processes the image without error.
    test_image = Image.open("tests/test_images/Chihuahua.png")
    result = classify_image(test_image)
    
    assert isinstance(result, str), "Prediction should return a class label."
    assert len(result) > 0, "Prediction should not return an empty string."
    assert result == "Chihuahua", "Prediction should classify the test image as a Chihuahua."
