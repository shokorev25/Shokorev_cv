def prefix_to_infix(expression: str) -> str:
    if not expression:
        raise ValueError("Выражение не должно быть пустым")
    
    tokens = expression.split()
    stack = []

    for token in reversed(tokens):
        if token.isdigit():  
            stack.append(token)
        elif token in {"+", "-", "*", "/"}:  
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов")
            operand1 = stack.pop()
            operand2 = stack.pop()
            stack.append(f"({operand1} {token} {operand2})")
        else:
            raise ValueError(f"Недопустимый символ: {token}")

    if len(stack) != 1:
        raise ValueError("Некорректное выражение: проверьте баланс операторов и операндов")

    return stack[0]

if __name__ == "__main__":
    expression = input("Введите выражение в префиксной нотации: ")
    try:
        result = prefix_to_infix(expression)
        print("Инфиксная запись:", result)
    except ValueError as e:
        print("Ошибка:", e)
