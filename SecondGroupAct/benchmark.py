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

