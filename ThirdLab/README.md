1. Differentiate Task and Data Parallelism. Identify which part of the lab demonstrates each and justify the workload division.
- Task Parallelism executes different computations on the same data, as shown in Part A where multiple deductions are calculated concurrently for one employee. Data Parallelism executes the same computation on different data, as shown in Part B where the same payroll function is applied to multiple employees. The workload division in Part A is by task, while in Part B it is by employee.

2. Explain how concurrent.futures managed execution, including submit(), map(), and Future objects. Discuss the purpose of with when creating an Executor.
- The concurrent.futures module manages concurrency by scheduling tasks through executors. submit() schedules individual tasks and returns Future objects, while map() applies the same function across multiple inputs. Future objects represent pending results, and the with statement ensures proper task completion and resource cleanup.

3. Analyze ThreadPoolExecutor execution in relation to the GIL and CPU cores. Did true parallelism occur?
- ThreadPoolExecutor does not achieve true parallelism for CPU-bound tasks due to the Global Interpreter Lock, which allows only one thread to execute Python bytecode at a time. Although tasks run concurrently, execution is interleaved on a single core rather than parallel across multiple cores.

4. Explain why ProcessPoolExecutor enables true parallelism, including memory space separation and GIL behavior.

5. Evaluate scalability if the system increases from 5 to 10,000 employees. Which approach scales better and why?

6. Provide a real-world payroll system example. Indicate where Task Parallelism and Data Parallelism would be applied, and which executor you would use.