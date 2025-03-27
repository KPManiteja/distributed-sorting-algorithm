# Use an official Python image as the base image
FROM python:3.10-slim

# Install MPI and Python libraries
RUN apt-get update && apt-get install -y \
    mpich \
    && pip install --no-cache-dir mpi4py numpy \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python script into the container
COPY distributed_sort.py /app/distributed_sort.py

# Set the working directory
WORKDIR /app

# Set the entry point to run the script with MPI
ENTRYPOINT ["mpiexec", "-n", "4", "python", "distributed_sort.py"]