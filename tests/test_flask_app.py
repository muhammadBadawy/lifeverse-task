import pytest
from flask_app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 404  # Because no / route is defined

def test_classify_no_file(client):
    response = client.post('/classify', data={})
    assert response.status_code == 400
    assert b"No file part" in response.data

def test_classify_empty_file(client):
    data = {'file': (b'', '')}
    response = client.post('/classify', data=data)
    assert response.status_code == 400
    assert b"No selected file" in response.data

def test_classify_valid_image(client):
    with open('tests/test_images/Chihuahua.png', 'rb') as img:
        data = {'file': (img, 'tests/test_images/Chihuahua.png')}
        response = client.post('/classify', data=data, content_type='multipart/form-data')
        print(response)
        assert response.status_code == 200
        
        # Extract the JSON response data
        json_data = response.get_json()
        
        classification = json_data.get('class', None)
        
        # Check if the classification key exists in the response data
        assert 'class' in json_data, "Response JSON should contain 'class' key."
        assert classification is not None, "Classification should not be None."
        assert classification == "Chihuahua", "Prediction should classify the test image as a Chihuahua."
