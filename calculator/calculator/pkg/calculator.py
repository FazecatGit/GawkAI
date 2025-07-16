def calculate(expression):
    print(f"Calculating: {expression}")
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    print(calculate("3+3/2"))