import time
import random
from mpi4py import MPI

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        print("Error: This simulation requires at least 2 processes.")
        return

    # --- MASTER PROCESS (Rank 0) ---
    if rank == 0:
        print(f"=== [Master Process {rank}] Initializing System ===")
        order_pool = [
            {"id": 101, "item": "Laptop"}, {"id": 102, "item": "Smartphone"},
            {"id": 103, "item": "Headphones"}, {"id": 104, "item": "Mechanical Keyboard"},
            {"id": 105, "item": "Gaming Mouse"}, {"id": 106, "item": "Monitor"}
        ]
        orders = order_pool[:random.randint(5, len(order_pool))]
        print(f"[Master] Distributing {len(orders)} orders.\n")

        # Distribute Tasks
        for i, order in enumerate(orders):
            worker_rank = (i % (size - 1)) + 1
            comm.send(order, dest=worker_rank, tag=1)

        # Stop signal
        for worker_rank in range(1, size):
            comm.send(None, dest=worker_rank, tag=1)

        # Collect results via MPI gathering instead of shared memory
        completed_orders = []
        for worker_rank in range(1, size):
            worker_results = comm.recv(source=worker_rank, tag=2)
            completed_orders.extend(worker_results)

        print("\n=== [Master] All workers finished. Fetching Results ===")
        for completed in completed_orders:
            print(f" -> Order #{completed['id']} [{completed['item']}] processed by Worker {completed['processed_by']}")

    # --- WORKER PROCESSES (Ranks > 0) ---
    else:
        my_processed_orders = []
        while True:
            order = comm.recv(source=0, tag=1)
            if order is None:
                break
            
            print(f"[Worker {rank}] Received Order #{order['id']}: {order['item']}")
            delay = random.uniform(1.0, 3.0) 
            time.sleep(delay)
            
            order['processed_by'] = rank
            my_processed_orders.append(order)
            print(f"    [DONE] [Worker {rank}] Finished Order #{order['id']} (Took {delay:.2f}s)")

        # Send locally tracked list back to master (No locks needed!)
        comm.send(my_processed_orders, dest=0, tag=2)

if __name__ == "__main__":
    main()