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


def data_parallelism_demo():
    salaries = [30000, 40000, 50000, 60000, 70000]

    with ProcessPoolExecutor() as executor:
        results = executor.map(payroll_computation, salaries)

    print("\n--- Data Parallelism Results ---")
    for i, result in enumerate(results, start=1):
        print(f"\nEmployee {i} (Process ID: {result['process_id']})")
        print(f"Gross Salary: ₱{result['gross_salary']:.2f}")
        print(f"Total Deduction: ₱{result['total_deduction']:.2f}")
        print(f"Net Salary: ₱{result['net_salary']:.2f}")


if __name__ == "__main__":
    data_parallelism_demo()
