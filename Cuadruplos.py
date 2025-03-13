import re

def obtener_prioridad(op):
    prioridades = {'+': 1, '-': 1, '*': 2, '/': 2}
    return prioridades.get(op, 0)

def convertir_a_postfija(expresion):
    salida = []
    pila = []
    tokens = re.findall(r'\d+|[a-zA-Z]+|[+\-*/()]', expresion)
    
    for token in tokens:
        if token.isalnum():  # Si es número o variable
            salida.append(token)
        elif token in {'+', '-', '*', '/'}:
            while pila and pila[-1] != '(' and obtener_prioridad(pila[-1]) >= obtener_prioridad(token):
                salida.append(pila.pop())
            pila.append(token)
        elif token == '(':
            pila.append(token)
        elif token == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop()  # Eliminar '('
    
    while pila:
        salida.append(pila.pop())
    
    return salida

def generar_cuadruplos(expresion):
    postfija = convertir_a_postfija(expresion)
    pila = []
    cuadruplos = []
    temp_count = 1
    
    for token in postfija:
        if token.isalnum():
            pila.append(token)
        else:  # Es un operador
            op2 = pila.pop()
            op1 = pila.pop()
            temp_var = f't{temp_count}'
            cuadruplos.append((token, op1, op2, temp_var))
            pila.append(temp_var)
            temp_count += 1
    
    return cuadruplos

if __name__ == "__main__":
    expresion = input("Ingrese la expresión matemática: ")
    cuadruplos = generar_cuadruplos(expresion)
    print("\nCuádruplos generados:")
    for i, cuad in enumerate(cuadruplos, 1):
        print(f"{i}. {cuad}")
