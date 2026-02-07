1. Which approach demonstrates true parallelism in Python? Explain.

Multiprocessing demonstrates true parallelism. Each process has its own memory space and Python interpreter, bypassing the GIL. This allows multiple CPU cores to execute simultaneously.

2. Compare execution times between multithreading and multiprocessing.

CPU-bound tasks (e.g., heavy calculations): Multiprocessing is faster, leveraging multiple cores.

I/O-bound tasks (e.g., time.sleep, file I/O): Multithreading can be faster or comparable, as threads are lightweight and the GIL is released during I/O.

In this lab (using time.sleep to simulate I/O), multithreading may perform similarly or slightly better due to lower overhead.

3. Can Python handle true parallelism using threads? Why or why not.

No. CPython threads cannot achieve true parallelism for CPU-bound tasks because of the GIL, which allows only one thread to execute Python bytecode at a time. Threads provide concurrency (task switching) rather than simultaneous execution.

4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster and why?

Multiprocessing would be faster for CPU-heavy computations, as multiple cores process grades simultaneously.

Multithreading would be slower due to threads competing for the GIL, adding overhead without speed gains.

5. Which method is better for CPU-bound tasks and which for I/O-bound tasks?

CPU-bound: Multiprocessing

I/O-bound: Multithreading

6. How did your group apply creative coding or algorithmic solutions in this lab?

Dynamic Input: Allowed input of the number of students and subjects for flexible testing.

Detailed Output: Displayed GWA and execution time for each thread/process to highlight concurrency/parallelism.

Error Handling & Structure: Clean separation of tasks by assigning specific data chunks to each worker.