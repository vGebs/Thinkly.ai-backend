# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run gunicorn when the container launches
CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:3000", "--timeout", "200", "server:app"]
