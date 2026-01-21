def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Error: Division by zero"

while True:
    op = input("Operation (+ - * /) or 'exit': ")

    if op == 'exit':
        break

    if op in ['+', '-', '*', '/']:
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))

            if op == "+":
                result = add(a, b)
            elif op == "-":
                result = subtract(a, b)
            elif op == "*":
                result = multiply(a, b)
            elif op == "/":
                result = divide(a, b)

            print(f"Result: {result}")
        except ValueError:
            print("Invalid input. Please enter numbers.")
    else:
        print("Invalid operation. Please choose +, -, *, / or 'exit'.")















