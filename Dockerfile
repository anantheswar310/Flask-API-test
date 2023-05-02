# Use an official Python runtime as a parent image
FROM ubuntu:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app to listen on
EXPOSE 8080

# Start the Flask app
ENTRYPOINT  ["python3"]
CMD ["BooksApi.py"]