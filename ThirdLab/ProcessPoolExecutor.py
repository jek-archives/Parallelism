from concurrent.futures import ProcessPoolExecutor
import os

def payroll_computation(salary):
    sss = salary * 0.04
    philhealth = salary * 0.025
    pagibig = salary * 0.02
    tax = salary * 0.10

    total_deduction = sss + philhealth + pagibig + tax
    net_salary = salary - total_deduction

    return {
        "process_id": os.getpid(),
        "gross_salary": salary,
        "total_deduction": total_deduction,
        "net_salary": net_salary
    }



