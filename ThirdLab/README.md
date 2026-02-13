1. Differentiate Task and Data Parallelism. Identify which part of the lab demonstrates each and justify the workload division.
- Task Parallelism executes different computations on the same data, demonstrated in Part A where independent deduction functions run concurrently on one salary. Data Parallelism executes the same computation on different data, demonstrated in Part B where one payroll function is applied to multiple employees. The workload is divided by task in Part A and by employee in Part B.

2. Explain how concurrent.futures managed execution, including submit(), map(), and Future objects. Discuss the purpose of with when creating an Executor.
- concurrent.futures manages concurrency through executors that schedule asynchronous tasks. submit() schedules individual tasks and returns Future objects, while map() applies a single function across multiple inputs. Future objects represent pending results, and the with statement ensures orderly shutdown and resource cleanup.

3. Analyze ThreadPoolExecutor execution in relation to the GIL and CPU cores. Did true parallelism occur?
- ThreadPoolExecutor does not provide true parallelism for CPU-bound tasks because the Global Interpreter Lock restricts execution to one thread at a time. Although multiple threads are scheduled, execution is interleaved rather than parallel across CPU cores.

4. Explain why ProcessPoolExecutor enables true parallelism, including memory space separation and GIL behavior.
- ProcessPoolExecutor enables true parallelism by using separate processes with independent memory spaces and GILs. This allows simultaneous execution on multiple CPU cores without interpreter-level contention.

5. Evaluate scalability if the system increases from 5 to 10,000 employees. Which approach scales better and why?
- Data Parallelism scales better as workload size increases because identical computations can be distributed across processes and CPU cores. Task Parallelism does not scale efficiently since the number of tasks per employee is limited.

6. Provide a real-world payroll system example. Indicate where Task Parallelism and Data Parallelism would be applied, and which executor you would use.
- In a real payroll system, Task Parallelism would be used to compute multiple deductions for a single employee, while Data Parallelism would be used to process payroll for large numbers of employees. ThreadPoolExecutor suits task-level concurrency, while ProcessPoolExecutor is appropriate for large-scale payroll computation.