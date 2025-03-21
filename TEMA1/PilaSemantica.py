def evaluar_expresion(expresion):
    operadores = []  # Pila para operadores (+, -, *, /)
    operandos = []   # Pila para operandos (números)

    # Precedencia de operadores
    precedencia = {'+': 1, '-': 1, '*': 2, '/': 2}

    def procesar_operador():
        """Extrae operandos y operadores para realizar la operación y apilar el resultado."""
        operador = operadores.pop()
        b = operandos.pop()
        a = operandos.pop()

        if operador == '+':
            operandos.append(a + b)
        elif operador == '-':
            operandos.append(a - b)
        elif operador == '*':
            operandos.append(a * b)
        elif operador == '/':
            if b == 0:
                raise ZeroDivisionError("Error: División por cero.")
            operandos.append(a / b)

    i = 0
    while i < len(expresion):
        char = expresion[i]

        if char.isdigit():  # Si es número, agrupar si hay varios dígitos
            num = char
            while i + 1 < len(expresion) and expresion[i + 1].isdigit():
                num += expresion[i + 1]
                i += 1
            operandos.append(int(num))

        elif char in precedencia:  # Si es operador
            while (operadores and operadores[-1] in precedencia and 
                   precedencia[operadores[-1]] >= precedencia[char]):
                procesar_operador()
            operadores.append(char)

        elif char == '(':  # Si es paréntesis de apertura
            operadores.append(char)

        elif char == ')':  # Si es paréntesis de cierre, procesar hasta '('
            while operadores and operadores[-1] != '(':
                procesar_operador()
            operadores.pop()  # Eliminar '('

        i += 1

    while operadores:
        procesar_operador()

    return operandos[0]  # Resultado final

# Prueba con expresiones
expresiones = ["3 + 4 * 2", "5 + 3 * 2 - 1", "(2 + 3) * 4", "10 / 2 + 6 * 3 - 4"]
for exp in expresiones:
    resultado = evaluar_expresion(exp.replace(" ", ""))  # Quitar espacios
    print(f"{exp} = {resultado}")