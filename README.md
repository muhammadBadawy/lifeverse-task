# Animal Classifier Web Application

This repository contains an animal classification web application that uses a pre-trained ResNet model for classifying images. The project is built using Flask, with separate unit tests using `pytest` and Continuous Integration/Continuous Deployment (CI/CD) pipelines for Google Cloud Build. 

app endpoint:
```
https://animal-classifier-643608676299.us-central1.run.app/classify
```

## Table of Contents
- [Application Overview](#application-overview)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Setting Up the Environment](#setting-up-the-environment)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [CI/CD Pipelines](#cicd-pipelines)
  - [PR Checks](#pr-checks-pipeline)
  - [Release](#release-pipeline)
  - [Deploy](#deploy-pipeline)

## Application Overview

The application is a Flask-based web service that accepts image uploads and classifies them using a pre-trained ResNet model from the `torchvision` library.

## Requirements
Make sure to install these dependencies using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Project Structure
```
/image-classification-app
	/flask_app.py # Main Flask application
	/streamlit_app.py # Main Flask application
	/requirements.txt # Dependencies
	/tests/
		/test_flask_app.py # Unit tests for flask using pytest
		/test_flask_app.py # Unit tests for streamlit using pytest
	/Dockerfile # Docker configuration
	/cicd # CICD pipeline configs for Google Cloud Build
		/pr-checks.yaml
		/release.yaml
		/deploy.yaml
	/config.json # selectedx model configuration
	/models # folder to download model artifacts
```
## Setting Up the Environment

Install the required dependencies using the provided `requirements.txt` file.
```
pip install -r requirements.txt
```
## Running the Application
To start the Flask web server, run the following command:
```
python app.py
```
By default, the application will be accessible at `http://127.0.0.1:5000/`.

### API Endpoint

-   **POST /classify**: This endpoint accepts an image file and returns a JSON response with the predicted class.

Example cURL request:
```
curl -X POST -F "file=@path_to_your_image.jpg" http://127.0.0.1:5000/classify
```
### Running Tests
The project uses `pytest` for unit testing. To run the tests, execute the following command:
```
pytest
```

## CI/CD Pipelines

Three Google Cloud Build CI/CD pipelines have been created to ensure a smooth workflow for testing, building, and deploying the application.

![image](https://github.com/user-attachments/assets/b4c62b8e-b93f-4849-8659-b5048eb2ad0a)

### PR Checks Pipeline

This pipeline runs automatically when a pull request is made to the `main` branch. It performs linting and runs unit tests. The steps include:

1.  **Install dependencies**: The `requirements.txt` file is used to install the necessary Python packages.
2.  **Linting**: The `pylint` tool is used for code quality checks. The pylint score is required to be above 7.
3.  **Run Tests**: The `pytest` command runs unit tests, ensuring code quality.
```
steps:
  - name: 'python:3.9'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        pip install -r requirements.txt
        export PYTHONPATH=$(pwd)
        pylint --disable=R,C --fail-under=7 flask_app.py streamlit_app.py model_loader.py
        pytest --maxfail=1 --disable-warnings
timeout: "1200s"
options:
  logging: CLOUD_LOGGING_ONLY

```
### Release Pipeline
This pipeline runs when code is merged into the `main` branch. It builds the Docker image and pushes it to Google Cloud's Artifact Registry. The steps include:

1.  **Build Docker Image**: A Docker image for the application is built using the `Dockerfile`.
2.  **Push Docker Image**: The built image is pushed to the Artifact Registry.
```
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'us-central1-docker.pkg.dev/$_PROJECT_ID/lifeverse/animal_classifier:latest'
      - '.'
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'us-central1-docker.pkg.dev/$_PROJECT_ID/lifeverse/animal_classifier:latest'
images:
  - 'us-central1-docker.pkg.dev/$_PROJECT_ID/lifeverse/animal_classifier:latest'
timeout: '1200s'
options:
  logging: CLOUD_LOGGING_ONLY
```
### Deploy Pipeline
This pipeline is triggered when a new release with a tag is created. It deploys the Docker image to Google Cloud Run. The steps include:

1.  **Deploy Docker Image**: The previously built image is deployed to Cloud Run using the `gcloud` command-line tool.
```
steps:
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        gcloud run deploy $_SERVICE_NAME \
          --image $_IMAGE \
          --platform managed \
          --region $_REGION \
          --allow-unauthenticated \
          --port $_PORT \
          --cpu 2 \
          --memory 4096Mi \
          --max-instances 1
timeout: 1200s
options:
  logging: CLOUD_LOGGING_ONLY

```
