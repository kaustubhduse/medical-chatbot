# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies for sounddevice
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run the Streamlit app when the container launches
CMD ["streamlit", "run", "app.py"]
