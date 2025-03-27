import os
from mpi4py import MPI
import numpy as np
import time
import logging

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Rank of the current process
size = comm.Get_size()  # Total number of processes

# Set up logging
logging.basicConfig(level=logging.INFO, format=f"Node {rank}: %(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Master node (rank 0) generates and divides the data
if rank == 0:
    # Generate a large dataset of random numbers
    data_size = 1000 # Configurable data size
    data = np.random.randint(0, 10000, data_size)
    logging.info(f"Generated data of size {data_size}")
    chunks = np.array_split(data, size)  # Divide data into chunks
else:
    chunks = None

# Scatter chunks to all nodes
local_data = comm.scatter(chunks, root=0)

# Simulate node failure (e.g., Node 2 fails)
if rank == 2:
    logging.error("Node 2 failed!")
    local_data_sorted = None
else:
    # Each node sorts its chunk
    start_time = time.time()
    local_data_sorted = np.sort(local_data)
    end_time = time.time()
    logging.info(f"Sorted data in {end_time - start_time:.4f} seconds")

# Gather sorted chunks at the master node
sorted_chunks = comm.gather(local_data_sorted, root=0)

# Master node merges the sorted chunks
if rank == 0:
    # Handle failed nodes (remove None values)
    sorted_chunks = [chunk for chunk in sorted_chunks if chunk is not None]
    final_sorted_data = np.concatenate(sorted_chunks)
    
    # Display final sorted data in a readable format
    logging.info("Final Sorted Data:")
    print(final_sorted_data)  
   

git remote add origin https://github.com/KPManiteja/distributed-sorting-algorithm.git