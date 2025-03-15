# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Install additional dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Expose the port
EXPOSE 8501

# Run the command to start the Streamlit app
CMD ["streamlit", "run", "app.py"]