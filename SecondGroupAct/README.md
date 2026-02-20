Group Members: Rabaya, Quejada, Libutan, Tuazon, Bajarla

Parallel and Distributed Computing

Second Group Activity: The “Analog-to-Digital” Parallel Challenge

**Real-World Bottleneck Discovery**

\- In a typical clinic environment, the triage desk serves as the first point of patient intake. A single triage nurse is usually responsible for the entire triage process, which includes collecting patient information, measuring vital signs, conducting symptom interviews, and assigning a priority level. Each patient must complete all these steps before the next patient can be accommodated, resulting in a strictly sequential workflow.

**What Is the Current Bottleneck?**

\- The primary bottleneck in this system is the reliance on a single triage nurse to process all patients from start to finish. During peak clinic hours, patients form long queues because only one patient can be assessed at any given time, regardless of how simple or repetitive the triage tasks may be.

**Why It Limits Efficiency**

\- The triage desk limits efficiency because vital sign collection, symptom documentation, and preliminary assessment are largely independent across patients but are forced to occur sequentially. Since a single nurse performs all triage activities end-to-end, overall throughput is constrained by individual processing speed. As patient volume increases, waiting times grow significantly even though multiple patients could be assessed simultaneously without compromising accuracy or safety.

**Type of Parallelism Required**

\- The most appropriate improvement strategy for this system is data parallelism. Each patient represents an independent data entity undergoing the same set of triage operations. By allowing multiple workers to process different patients concurrently using identical procedures, throughput can be increased without altering the logical structure of the triage process.

**Parallel Mapping**

**Define the Work Unit**

\- In the computational model, a single patient triage record is defined as the smallest independent unit of computation. This unit includes measuring vital signs, recording symptoms, assigning a priority level, and saving the record. Because these steps are repeated uniformly for every patient, each triage record can be processed independently of others.

**Identify System Constraints**

\- Parallel execution in the clinic triage model is limited by several practical constraints. The electronic medical record system functions as a shared resource that requires synchronized access, creating a critical section in the workflow. Physical triage equipment, such as blood pressure monitors and thermometers, may be limited in number, leading to contention among workers. Additionally, coordination overhead and thread management costs restrict how efficiently the system can scale as more workers are added.

**Select and Justify the Parallel Strategy**

\- Data parallelism is the most suitable optimization strategy for the clinic triage desk.   
Each patient represents an independent unit of data that undergoes the same triage procedure, allowing multiple workers to process different patients concurrently.   
Synchronization is only necessary when accessing shared resources such as patient records, making data parallelism both effective and realistic for this scenario.

**Flowchart**

PNG in docs file submitted in a diff file.

**Implementation (Benchmark)**

PNG in docs file submitted in a diff file.
