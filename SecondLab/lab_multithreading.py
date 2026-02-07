import time
from threading import Thread

def compute_gwa(grades, id):
    start_time = time.time()
    # Simulate computation
    time.sleep(0.1)
    gwa = sum(grades) / len(grades)
    end_time = time.time()
    duration = end_time - start_time
    print(f"[Thread {id}] Finished | GWA: {gwa:.2f} | Time taken: {duration:.6f} seconds")

# Input grades
num_students = int(input("How many students? "))
num_subjects = int(input("How many subjects? "))
all_grades = []

for i in range(num_students):
    grades = []
    print(f"\nEnter grades for student {i+1}:")
    for j in range(num_subjects):
        grade = float(input(f"Enter grade {j+1}: "))
        grades.append(grade)
    all_grades.append(grades)

# Compute GWA with threads
print("\n=== Multithreading GWA Computation ===")
threads = []
start_time = time.time()

for idx, grades_list in enumerate(all_grades, start=1):
    t = Thread(target=compute_gwa, args=(grades_list, idx))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time = time.time()
print(f"\n[Multithreading] Total Execution Time: {end_time - start_time:.4f} seconds")
