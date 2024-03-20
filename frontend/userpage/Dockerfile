# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /home/ubuntu/StepUpSage_FE/userpage/

# Copy the current directory contents into the container at /deploy/Deploy.Ai/frontend
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements/requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Install Supervisor
RUN apt-get update && apt-get install -y supervisor

# Create and set permissions for the Gunicorn log directory
RUN mkdir -p /var/log/gunicorn && \
    chown -R nobody:nogroup /var/log/gunicorn

# Copy the Supervisor config file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run Supervisor when the container launches
CMD ["/usr/bin/supervisord"]

#TEST Comment
