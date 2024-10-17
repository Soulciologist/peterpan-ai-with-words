# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Command to run the Flask app
# CMD ["python", "run.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
