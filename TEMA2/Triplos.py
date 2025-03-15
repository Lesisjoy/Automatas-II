import re

# Función para convertir una expresión infija a postfija
def infija_a_postfija(expresion):
    precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}  # Precedencia de operadores
    pila = []
    postfija = []
    
    # Función para verificar si un carácter es un operador
    def es_operador(caracter):
        return caracter in precedencia
    
    # Función para verificar si un carácter es un paréntesis
    def es_parentesis(caracter):
        return caracter in ['(', ')']
    
    # Recorrer la expresión infija
    for caracter in expresion:
        if caracter.isdigit() or caracter.isalpha():  # Si es un número o variable
            postfija.append(caracter)
        elif es_operador(caracter):  # Si es un operador
            while (pila and es_operador(pila[-1]) and 
                   precedencia[pila[-1]] >= precedencia[caracter]):
                postfija.append(pila.pop())
            pila.append(caracter)
        elif caracter == '(':  # Si es un paréntesis de apertura
            pila.append(caracter)
        elif caracter == ')':  # Si es un paréntesis de cierre
            while pila and pila[-1] != '(':
                postfija.append(pila.pop())
            pila.pop()  # Eliminar '(' de la pila
    
    # Vaciar la pila
    while pila:
        postfija.append(pila.pop())
    
    return postfija

# Función para generar triplos a partir de una expresión postfija
def generar_triplos(expresion_postfija):
    pila = []  # Pila para almacenar operandos y temporales
    triplos = []  # Lista para almacenar los triplos generados
    contador_temporal = 1  # Contador para generar nombres de temporales

    for elemento in expresion_postfija:
        if elemento.isdigit() or elemento.isalpha():  # Si es un número o variable
            pila.append(elemento)
        else:  # Si es un operador
            operando2 = pila.pop()
            operando1 = pila.pop()
            temporal = f"t{contador_temporal}"  # Generar nombre de temporal
            triplos.append((elemento, operando1, operando2))  # Agregar triplo
            pila.append(temporal)  # Apilar el resultado temporal
            contador_temporal += 1  # Incrementar el contador de temporales

    return triplos

# Función principal
def main():
    # Solicitar la expresión infija al usuario
    expresion_infija = input("Ingresa una expresión infija (por ejemplo, '((6+4)/2)+3'): ")
    
    # Convertir la expresión infija a postfija
    expresion_postfija = infija_a_postfija(expresion_infija)
    print("Expresión postfija:", " ".join(expresion_postfija))
    
    # Generar triplos a partir de la expresión postfija
    triplos = generar_triplos(expresion_postfija)
    
    # Imprimir los triplos generados
    print("\nTriplos generados:")
    for i, triplo in enumerate(triplos, start=1):
        print(f"{i}: {triplo}")

# Ejecutar el programa
if __name__ == "__main__":
    main()