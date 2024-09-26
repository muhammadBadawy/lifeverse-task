# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy the poetry.lock and pyproject.toml files
COPY ./* ./

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --no-dev

# Copy the rest of the application code
COPY . .

# Download the model and labels
RUN python -m poetry run python -c "from model_loader import initialize_model; initialize_model()"

# Optionally set the entrypoint for the container (if applicable)
# CMD ["python", "flask_app.py", "--host=0.0.0.0", "--port=8501"]  # Uncomment if you want to run the app in the container
