# We start with an image that has Python 3.11.3 installed
FROM python:3.11.3

# Set a directory for the application
WORKDIR /usr/src/app

# Copy requirements.txt file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the command to start your application
CMD ["flask", "run"]
