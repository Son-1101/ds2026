from mpi4py import MPI
import os

# Configuration
CHUNK_SIZE = 4096
TAG_FILENAME = 1
TAG_DATA = 2
TAG_END = 3

def run_sender(comm, dest_rank):
    """Sender Logic (Rank 0) - Acts as Client"""
    # Changed input prompt to English to avoid encoding errors
    filename = input("Rank 0 (Sender) - Please enter filename to send (e.g., test.txt): ").strip()
    
    if not os.path.isfile(filename):
        print(f"[-] Rank 0: File '{filename}' not found.")
        # Send end signal so receiver doesn't wait forever
        comm.send(None, dest=dest_rank, tag=TAG_END)
        return

    # 1. Send Filename
    print(f"[*] Rank 0: Sending filename '{filename}'...")
    comm.send(filename, dest=dest_rank, tag=TAG_FILENAME)

    # 2. Send File Content
    print("[*] Rank 0: Sending file content...")
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            # Send chunk
            comm.send(chunk, dest=dest_rank, tag=TAG_DATA)
    
    # 3. Send End Signal
    comm.send(None, dest=dest_rank, tag=TAG_END)
    print("[+] Rank 0: Transfer finished.")

def run_receiver(comm, source_rank):
    """Receiver Logic (Rank 1) - Acts as Server"""
    print("[*] Rank 1 (Receiver): Waiting for data...")
    f = None

    while True:
        # Receive data and check tag
        status = MPI.Status()
        data = comm.recv(source=source_rank, tag=MPI.ANY_TAG, status=status)
        tag = status.Get_tag()

        if tag == TAG_FILENAME:
            # Receive Filename
            filename = os.path.basename(data)
            output_file = "received_" + filename
            print(f"[*] Rank 1: Received filename '{filename}'. Saving to '{output_file}'")
            f = open(output_file, 'wb')

        elif tag == TAG_DATA:
            # Receive Data Chunk
            if f:
                f.write(data)
        
        elif tag == TAG_END:
            # Receive End Signal
            print("[+] Rank 1: File transfer complete.")
            if f:
                f.close()
            break

if __name__ == "__main__":
    # Initialize MPI environment
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank() 
    size = comm.Get_size() 

    # Require at least 2 processes
    if size < 2:
        print("[-] Error: Need at least 2 processes (Sender & Receiver)")
        print("    Run with: mpiexec -n 2 python mpi_transfer.py")
        exit(1)

    if rank == 0:
        # Rank 0 is Sender
        run_sender(comm, dest_rank=1)
    elif rank == 1:
        # Rank 1 is Receiver
        run_receiver(comm, source_rank=0)