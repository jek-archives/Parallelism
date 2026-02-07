# Lab Report: Multithreading vs Multiprocessing

## 3. Execution Time Comparison

| Method | Execution Order | GWA Output | Execution Time |
| :--- | :--- | :--- | :--- |
| **Multithreading** | Concurrent (Interleaved) | Printed as threads finish | *[Record Time Here]* |
| **Multiprocessing** | Parallel (Independent) | Printed as processes finish | *[Record Time Here]* |

**Discussion:**
- **Multithreading:** Threads may finish in a non-deterministic order depending on the OS scheduler, but due to the GIL, they run concurrently rather than truly in parallel for CPU-bound tasks.
- **Multiprocessing:** Processes run independently and truly in parallel on separate CPU cores, so their finish order is also non-deterministic but based on true simultaneous execution.

## 4. Question & Answer

### 1. Which approach demonstrates true parallelism in Python? Explain.
**Multiprocessing** demonstrates true parallelism. Each process runs in its own memory space with its own Python interpreter instance. This bypasses the Global Interpreter Lock (GIL), allowing multiple CPU cores to be utilized simultaneously for computation.

### 2. Compare execution times between multithreading and multiprocessing.
- For **CPU-bound tasks** (like heavy calculations), **Multiprocessing** is generally faster because it utilizes multiple cores.
- For **I/O-bound tasks** (like waiting for user input or `time.sleep`), **Multithreading** can be faster or comparable because threads are lighter weight to create and context switch than processes, and the GIL is released during I/O operations.
- In this specific lab, since we used `time.sleep` (simulating I/O), multithreading might actually perform similarly or slightly better due to lower overhead, despite not being "truly" parallel.

### 3. Can Python handle true parallelism using threads? Why or why not?
**No**, standard Python (CPython) cannot handle true parallelism using threads for CPU-bound tasks due to the **Global Interpreter Lock (GIL)**. The GIL ensures that only one thread executes Python bytecode at a time per process, effectively creating concurrency (task switching) rather than parallelism (simultaneous execution).

### 4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster and why?
If the task involves heavy computation for each of the 1000 grades:
- **Multiprocessing** would be significantly faster as it leverages multiple cores to process grades simultaneously.
- **Multithreading** would be slower because threads would fight for the single GIL execution slot, adding overhead without gaining speed.

### 5. Which method is better for CPU-bound tasks and which for I/O-bound tasks?
- **CPU-bound tasks:** **Multiprocessing** (bypasses GIL, uses multiple cores).
- **I/O-bound tasks:** **Multithreading** (lower overhead, GIL is released during I/O waiting).

### 6. How did your group apply creative coding or algorithmic solutions in this lab?
- **Dynamic Input:** Instead of hardcoding lists, we implemented a robust input system that asks for the number of students and subjects, allowing for dynamic testing.
- **Detailed Output:** We formatted the output to show not just the GWA but also the specific time taken by each thread/process to analyze the "simultaneous" nature of the execution.
- **Error Handling:** (Implicitly in design) We maintained clean separation of concerns by passing specific data chunks to each worker.
