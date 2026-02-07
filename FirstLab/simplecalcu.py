def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

if __name__ == "__main__":
    while True:
        op = input("Operation (+ - * /) or 'exit': ")
        if op == "exit":
            break
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))

            if op == "+":
                print(add(a, b))
                
            elif op == "-":
                print(subtract(a,b))
            
            elif op == "*":
                print(multiply(a, b))
            
            elif op == "/":
                result = divide(a, b)
                print(result)
        except ValueError:
            print("Invalid input")
    else:
        print("Invalid operation")

    print()   















