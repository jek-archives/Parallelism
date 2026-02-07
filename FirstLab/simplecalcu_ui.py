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

root = tk.Tk()
root.title("Persistent Calculator")

tk.Label(root, text="First Number").grid(row=0, column=0, padx=5, pady=5)
entry_a = tk.Entry(root)
entry_a.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Second Number").grid(row=1, column=0, padx=5, pady=5)
entry_b = tk.Entry(root)
entry_b.grid(row=1, column=1, padx=5, pady=5)

op_var = tk.StringVar(value="+")
tk.OptionMenu(root, op_var, "+", "-", "*", "/").grid(row=2, column=0, columnspan=2, pady=5)

tk.Button(root, text="Compute", command=compute).grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="Result: ")
result_label.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()
