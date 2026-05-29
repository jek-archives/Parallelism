import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

db_lock = Lock()

def triage_patient_parallel(patient_id):
    time.sleep(0.1)
    time.sleep(0.1)
    with db_lock:  # critical section
        time.sleep(0.05)

def parallel_triage(patients, workers=4):
    start = time.time()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(triage_patient_parallel, patients)
    end = time.time()
    return end - start

def triage_patient(patient_id):
    time.sleep(0.1)  # simulate vital signs
    time.sleep(0.1)  # simulate symptom interview
    time.sleep(0.05) # simulate database write

def sequential_triage(patients):
    start = time.time()
    for patient in patients:
        triage_patient(patient)
    end = time.time()
    return end - start

if __name__ == "__main__":
    NUM_PATIENTS = 40
    WORKERS = 6

    patients = list(range(NUM_PATIENTS))

    print("Running Sequential Triage...")
    seq_time = sequential_triage(patients)
    print(f"Sequential Time: {seq_time:.2f} seconds")

    print("\nRunning Parallel Triage...")
    par_time = parallel_triage(patients, WORKERS)
    print(f"Parallel Time: {par_time:.2f} seconds")

    speedup = seq_time / par_time
    print(f"\nSpeedup: {speedup:.2f}x")