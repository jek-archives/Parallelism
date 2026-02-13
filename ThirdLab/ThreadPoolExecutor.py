from concurrent.futures import ThreadPoolExecutor
import threading

# Deduction computation functions
def compute_sss(salary):
    print(f"SSS executed by {threading.current_thread().name}")
    return salary * 0.04

def compute_philhealth(salary):
    print(f"PhilHealth executed by {threading.current_thread().name}")
    return salary * 0.025

def compute_pagibig(salary):
    print(f"Pag-IBIG executed by {threading.current_thread().name}")
    return salary * 0.02

def compute_withholding_tax(salary):
    print(f"Withholding Tax executed by {threading.current_thread().name}")
    return salary * 0.10

def task_parallelism_demo():
    name = "Jake Kyotie"
    salary = 50000

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            "SSS": executor.submit(compute_sss, salary),
            "PhilHealth": executor.submit(compute_philhealth, salary),
            "Pag-IBIG": executor.submit(compute_pagibig, salary),
            "Withholding Tax": executor.submit(compute_withholding_tax, salary)
        }

        deductions = {}
        for name, future in futures.items():
            deductions[name] = future.result()

    total_deduction = sum(deductions.values())

    print("\n--- Task Parallelism Results ---")
    for name, amount in deductions.items():
        print(f"{name}: ₱{amount:.2f}")

    print(f"Total Deduction: ₱{total_deduction:.2f}")


if __name__ == "__main__":
    task_parallelism_demo()

