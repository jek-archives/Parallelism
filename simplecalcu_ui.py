import tkinter as tk
from simplecalcu import add, subtract, multiply, divide

def compute():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        op = op_var.get()

        if op == "+":
            result = add(a, b)
        elif op == "-":
            result = subtract(a, b)
        elif op == "*":
            result = multiply(a, b)
        elif op == "/":
            result = divide(a, b)
        else:
            result = "Select an operation"

        result_label.config(text=f"Result: {result}")
    except ValueError:
        result_label.config(text="Invalid input")


