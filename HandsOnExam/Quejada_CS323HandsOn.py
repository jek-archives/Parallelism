import time
from concurrent.futures import ThreadPoolExecutor


def process_order(order_id):
    
    print(f"Processing Order {order_id}...")

    #Verify order
    print(f"Order {order_id}: Verifying order")
    time.sleep(2)

    #Process payment
    print(f"Order {order_id}: Processing payment")
    time.sleep(3)

    #Packaging
    print(f"Order {order_id}: Packaging item")
    time.sleep(5)

    #Shipping preparation
    print(f"Order {order_id}: Ready for shipping")
    time.sleep(4)

    print(f"Order {order_id} completed.")


def main():
    print("=" * 50)
    print("ORDER PROCESSING SYSTEM")
    print("=" * 50)

    #atleast 10 orders
    orders = list(range(1, 13))
    print(f"Processing {len(orders)} orders...")
    print("-" * 50)

    start_time = time.time()

    #ThreadPoolExecutor to process orders
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(process_order, orders)

    end_time = time.time()

    print("-" * 50)
    print("All orders completed!")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    print("=" * 50)


if __name__ == "__main__":
    main()

# 1. Which concurrency tool did you use?
# ThreadPoolExecutor from the concurrent.futures module - it's like having a team of workers who can handle multiple orders at the same time instead of one person doing everything one-by-one.

# 2. Why did you select this approach?
# It's easy to use, works well for tasks that involve waiting (like I/O operations), and makes the program faster without being too complicated.

# 3. Is your program using task parallelism or data parallelism?
# Task parallelism bcs each order does multiple different tasks (verify, pay, package, ship) and multiple orders do these tasks at the same time.

# 4. Is this example primarily CPU-bound or I/O-bound?
# This is an exaple of I/O-bound bcs the program mostly waits (time.sleep) for things to happen instead of doing heavy calculations. In real life, it would wait for databases, networks, and file systems.

# 5. How does time.sleep represent real-world behavior?
# time.sleep pretends the program is waiting for real things like getting data from a database, talking to a payment service, or sending information over the internet.

# 6. How does concurrent processing improve performance?
# Instead of waiting for one order to finish completely before starting the next one, the program can start multiple orders at once. While one order is waiting for payment, another can be packaging.
# In the code I specifically put 3 workers to do the tasks at the same time.

# 7. What improvements for thousands of orders?
# Use a smaller worker pool size to avoid using too much memory, process orders in batches, or use async/await for even better performance with lots of I/O operations.
