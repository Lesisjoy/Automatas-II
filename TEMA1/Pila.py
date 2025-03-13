import re

def precedencia(operador):
    prioridad = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    return prioridad.get(operador, 0)

def infija_a_posfija(expresion):
    salida = []
    operadores = []
    tokens = re.findall(r'\d+\.\d+|\d+|[-+*/()^]', expresion)
    
    for token in tokens:
        if re.match(r'\d+', token):  # Si es número
            salida.append(token)
        elif token == '(':  # Si es paréntesis de apertura
            operadores.append(token)
        elif token == ')':  # Si es paréntesis de cierre
            while operadores and operadores[-1] != '(':
                salida.append(operadores.pop())
            if operadores:
                operadores.pop()  # Eliminar '('
            else:
                raise SyntaxError("Paréntesis desbalanceados en la expresión.")
        else:  # Es un operador
            while (operadores and operadores[-1] != '(' and
                   precedencia(operadores[-1]) >= precedencia(token)):
                salida.append(operadores.pop())
            operadores.append(token)
    
    while operadores:
        if operadores[-1] == '(':
            raise SyntaxError("Paréntesis desbalanceados en la expresión.")
        salida.append(operadores.pop())
    
    return ' '.join(salida)

def infija_a_prefija(expresion):
    expresion = expresion.replace(" ", "")  # Eliminar espacios para tokenización correcta
    tokens = re.findall(r'\d+\.\d+|\d+|[-+*/()^]', expresion)
    tokens = tokens[::-1]  # Invertir la lista de tokens
    tokens = [')' if t == '(' else '(' if t == ')' else t for t in tokens]
    
    expresion_invertida = ' '.join(tokens)
    expresion_posfija = infija_a_posfija(expresion_invertida)
    return ' '.join(expresion_posfija.split()[::-1])

# Ejemplo de uso
expresiones = [
    "5*4+((7/2)-3)",
    "(7+3)*5",
    "8-(4/2)+6"
]

for expresion in expresiones:
    try:
        print("Expresión infija:", expresion)
        print("Notación posfija:", infija_a_posfija(expresion))
        print("Notación prefija:", infija_a_prefija(expresion))
        print()
    except SyntaxError as e:
        print(f"Error en la expresión '{expresion}': {e}")
