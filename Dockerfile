# Use an official Anaconda runtime as a parent image
FROM continuumio/anaconda3:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD environment.yml /app
COPY . /app
# Update conda and install the necessary packages
RUN conda update -n base -c defaults conda && \
    conda env create -f environment.yml

# Activate the conda environment
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Expose port 5000 for Flask app
EXPOSE 5000

# Define the command to run the app
CMD ["conda", "run", "-n", "myenv", "python", "app.py"]
