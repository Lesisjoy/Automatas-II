def generar_codigo_intermedio(expresiones):
    # Diccionario para mapear operadores a sus respectivas prioridades
    precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
    
    # Función para verificar si un carácter es un operador
    def es_operador(caracter):
        return caracter in precedencia
    
    # Función para generar una nueva variable temporal
    temp_counter = 0
    def nueva_temp():
        nonlocal temp_counter
        temp = f'T{temp_counter}'
        temp_counter += 1
        return temp
    
    # Convertir la expresión infija a postfijo usando el algoritmo shunting-yard
    def infijo_a_postfijo(expresion):
        pila = []
        salida = []
        i = 0
        while i < len(expresion):
            caracter = expresion[i]
            if caracter == ' ':
                i += 1
                continue
            if caracter == '(':
                pila.append(caracter)
            elif caracter == ')':
                while pila and pila[-1] != '(':
                    salida.append(pila.pop())
                pila.pop()  # Eliminar el '('
            elif es_operador(caracter):
                while (pila and pila[-1] != '(' and
                       precedencia[pila[-1]] >= precedencia[caracter]):
                    salida.append(pila.pop())
                pila.append(caracter)
            else:
                # Es un operando (variable o número)
                # Manejar números de más de un dígito
                if caracter.isdigit():
                    num = ''
                    while i < len(expresion) and expresion[i].isdigit():
                        num += expresion[i]
                        i += 1
                    salida.append(num)
                    continue
                else:
                    salida.append(caracter)
            i += 1
        while pila:
            salida.append(pila.pop())
        return salida
    
    # Convertir la expresión infija a prefijo
    def infijo_a_prefijo(expresion):
        pila = []
        salida = []
        expresion = expresion[::-1]  # Invertir la expresión para facilitar el procesamiento
        i = 0
        while i < len(expresion):
            caracter = expresion[i]
            if caracter == ' ':
                i += 1
                continue
            if caracter == ')':
                pila.append(caracter)
            elif caracter == '(':
                while pila and pila[-1] != ')':
                    salida.append(pila.pop())
                pila.pop()  # Eliminar el ')'
            elif es_operador(caracter):
                while (pila and pila[-1] != ')' and
                       precedencia[pila[-1]] > precedencia[caracter]):
                    salida.append(pila.pop())
                pila.append(caracter)
            else:
                # Es un operando (variable o número)
                # Manejar números de más de un dígito
                if caracter.isdigit():
                    num = ''
                    while i < len(expresion) and expresion[i].isdigit():
                        num += expresion[i]
                        i += 1
                    salida.append(num[::-1])  # Invertir el número para restaurar su orden original
                    continue
                else:
                    salida.append(caracter)
            i += 1
        while pila:
            salida.append(pila.pop())
        return salida[::-1]  # Invertir la salida para obtener la notación prefija

    # Procesar cada expresión de la lista
    for expresion in expresiones:
        print(f"\nExpresión: {expresion}")
        
        # Convertir la expresión infija a prefija
        prefijo = infijo_a_prefijo(expresion)
        print("Notación prefija:", ' '.join(prefijo))
        
        # Convertir la expresión infija a postfijo
        postfijo = infijo_a_postfijo(expresion)
        print("Notación postfija:", ' '.join(postfijo))

# Lista de expresiones a evaluar
expresiones = [
    "(a + b) * (c -(d +e))",
    "(m + n) * (p - q) / r",
    "a + b * c - d / e"
]

#    "(a + b) * (c -(d +e))",
#    "((a + b) * c) + (d / e)",
#   "x * (y + z) - (w / v) + u",
#    "a * (b + c) - (d * e) / f",
#    "a / b * c / d",
#    "(a + b * c - (d / e + f) * g) / h",
#    "(a + (b * (c + (d - e)))) / f",
#    "(a - 8) + 7 * 16/4 + 13"

# Ejecutar el código con múltiples expresiones
generar_codigo_intermedio(expresiones)

