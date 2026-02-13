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



