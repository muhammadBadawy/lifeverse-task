FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . /app/

# Install Packages
RUN pip install -r requirements.txt

RUN python -c "from model_loader import initialize_model; initialize_model()"

# Expose the port Flask will run on
EXPOSE 5000

# Set the command to run the Flask app
CMD ["python", "flask_app.py", "--host=0.0.0.0", "--port=5000"]