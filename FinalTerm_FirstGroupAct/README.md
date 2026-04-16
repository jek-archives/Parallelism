
-Quejada Reflection
In this activity, I learned the difference between sequential and parallel execution. Sequential methods are faster for small datasets because they have no extra setup, while parallel methods use multiple processes but have overhead from creating and managing them. Based on the results, for 1,000 elements, sequential sorting was very fast at around 0.001 seconds, while parallel sorting took around 0.5 to 0.6 seconds. For 100,000 elements, sequential sorting was still faster at about 0.11 to 0.20 seconds compared to parallel at around 0.69 to 0.73 seconds. For 1,000,000 elements, parallel sorting became better in some cases, reaching around 1.25 to 1.72 seconds compared to sequential sorting at about 2.57 seconds. I also had difficulty splitting the dataset and combining the results from different processes. I learned that overhead affects performance, making parallel slower for small tasks but useful for large datasets. Overall, sequential is better for small tasks, while parallel is better when the dataset is very large.

-Libutan Reflection
The comparative implementation of sequential and parallel algorithms highlights clear differences in computational efficiency and execution models. Sequential approaches maintain stability and predictability due to their straightforward control flow and minimal overhead, making them suitable for smaller datasets. In contrast, parallel algorithms utilize concurrent processing to improve performance, though their advantages become evident only when handling sufficiently large workloads.

Despite these benefits, parallel execution introduces complexities such as process coordination, communication overhead, and synchronization requirements. These factors can negatively affect performance, particularly when the workload is not large enough to compensate for the added costs. As a result, the effectiveness of parallelism depends heavily on problem size and system efficiency.


-Tuazon Reflection
In this activity, we learned the difference between sequential and parallel algorithms by implementing sorting and searching using both approaches. Sequential algorithms execute tasks one step at a time, while parallel algorithms divide the work into smaller parts that can run at the same time using multiple processes. Through our testing, we were able to see how these two approaches behave when working with different dataset sizes.

When we tested the small dataset with 1,000 elements, the sequential algorithms were usually faster. This is because parallel algorithms have extra overhead, such as creating processes and coordinating results. For small tasks, this overhead sometimes takes longer than simply running the algorithm sequentially.

However, when we tested larger datasets like 100,000 and 1,000,000 elements, the parallel algorithms started to perform better. Since the data was divided into chunks and processed simultaneously, the program could use multiple CPU cores, which helped reduce the overall execution time.

One challenge we experienced was making sure the data was correctly divided and that the results from different processes were combined properly. For example, in the parallel sorting algorithm we had to merge sorted chunks correctly, and in the parallel search we had to return the correct index from different processes.

Overall, this activity helped us understand that parallel algorithms are useful for large workloads but not always necessary for smaller ones. It also showed us that while parallel computing can improve performance, it also makes the program more complex to design and manage.