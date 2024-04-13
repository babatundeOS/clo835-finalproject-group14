FROM ubuntu:20.04

# Update package lists and install required packages
RUN apt-get update -y && \
    apt-get install -y \
    python3-pip \
    mysql-client

# Set the working directory
WORKDIR /app

# Copy application code
COPY . /app

# Upgrade pip and install dependencies
RUN pip3 install --upgrade pip==21.3.1 && \
    pip3 install -r requirements.txt

# Expose port
EXPOSE 5000

# Create a non-root user
RUN groupadd -r appuser && \
    useradd -r -g appuser appuser

# Switch to non-root user
USER appuser

# Command to run the application
CMD ["python3", "app.py"]
