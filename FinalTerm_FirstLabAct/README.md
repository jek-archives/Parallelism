RABAYA, QUEJADA, LIBUTAN, TUAZON, BAJARLA


1. How did you distribute orders among worker processes?Orders were distributed by the Master process (rank 0) using a dynamic Round-Robin allocation strategy over MPI via comm.send(). The master looped through the list of generated orders and used the modulo operator (i % (size - 1)) + 1 to evenly cycle through available worker ranks (1 to $N$). Once all tasks were dispatched, the master sent a termination signal (None) to each worker to cleanly shut down their processing loops.

2. What happens if there are more orders than workers?
If there are more orders than workers, the system handles it gracefully because the master continuously loops through the available workers. The extra orders queue up and are processed sequentially. For example, if there are 3 workers and 7 orders, workers 1 and 2 will receive 2 orders each, while worker 3 will receive 3 orders. Workers will process their subsequent tasks immediately after completing their current one.

3. How did processing delays affect the order completion?
The introduction of randomized processing delays via time.sleep() decoupled task completion from the order in which tasks were assigned. Because workers executed their tasks completely independently in parallel, a worker assigned a later order with a short delay (e.g., 1.1s) would finish and log its results before a worker assigned an earlier order with a longer delay (e.g., 2.9s). This resulted in an out-of-order execution sequence reflecting a true asynchronous, real-world computing environment.

4. How did you implement shared memory, and where was it initialized?
Shared memory was implemented using the multiprocessing.Manager() class, specifically creating a manager.list().
Initialization Location: It was initialized globally at the start of the main() function before splitting the logic into master and worker execution blocks. This ensured that all parallel processes held an identical reference to the underlying IPC proxy server managing the memory state.

5. What issues occurred when multiple workers wrote to shared memory simultaneously?
When synchronization was removed, a Race Condition occurred. When multiple worker processes finished tasks at nearly the same microsecond, they attempted to mutate the shared memory pointer simultaneously. This resulted in data inconsistency issues such as:

Data Corruption: Memory collisions corrupting the array structure.

Dropped Logs: One worker overwriting another's write operation, leading to missing order entries in the final master summary.

6. How did you ensure consistent results when using multiple processes?
Consistent results were guaranteed by implementing mutual exclusion using a multiprocessing.Lock(). The shared lock object was passed to the workers, and the append operation was wrapped inside a with lock: context manager. This created a Critical Section, forcing workers to form an orderly queue. Even if multiple processes finished simultaneously, only one worker could acquire the lock and write to the shared list at any given millisecond, ensuring 100% data integrity and a complete final log for the master.