def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

while True:
    op = input("Operation (+ - * /) or 'exit': ")
    if op == "exit":
        break
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))

    if op == "+":
        print(add(a, b))
        
    elif op == "-":
        print(subtract(a,b))
    
    elif op == "*":
        print(multiply(a, b))
    
    elif op == "/":
        print(divide(a, b))
    else:
        print("Invalid operation")

    print()   















