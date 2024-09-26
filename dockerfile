FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir "poetry"

# Copy the project files to the container
COPY pyproject.toml poetry.lock /app/
COPY . /app/

# Install project dependencies using Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

RUN poetry run python -c "from model_loader import initialize_model; initialize_model()"

# Expose the port Flask will run on
EXPOSE 5000

# Set the command to run the Flask app
CMD ["poetry", "run", "python", "flask_app.py", "--host=0.0.0.0", "--port=5000"]