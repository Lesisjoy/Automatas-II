def generar_codigo_intermedio(expresion):
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
    
    # Convertir la expresión infija a postfija usando el algoritmo shunting-yard
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
    
    # Convertir la expresión infija a prefija
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
    
    # Generar código intermedio a partir de la notación postfija
    def postfijo_a_codigo_intermedio(postfijo):
        pila = []
        codigo_intermedio = []
        for token in postfijo:
            if es_operador(token):
                operando2 = pila.pop()
                operando1 = pila.pop()
                temp = nueva_temp()
                codigo_intermedio.append(f'{temp} = {operando1} {token} {operando2}')
                pila.append(temp)
            else:
                pila.append(token)
        if pila:
            codigo_intermedio.append(f'Z = {pila.pop()}')
        return codigo_intermedio
    
    # Convertir la expresión infija a prefija
    prefijo = infijo_a_prefijo(expresion)
    print("Notación prefija:", ' '.join(prefijo))
    
    # Convertir la expresión infija a postfija
    postfijo = infijo_a_postfijo(expresion)
    print("Notación postfija:", ' '.join(postfijo))
    
    
    # Generar el código intermedio
    codigo_intermedio = postfijo_a_codigo_intermedio(postfijo)
    return codigo_intermedio

# Ejemplo de uso
#expresion = "(m / n) + (p % q)"
#expresion = "(m + n) * (p - q) / r"
#expresion = "a + b * c - d / e"
#expresion = "(a + b) * (c -(d +e))"
#expresion = "((a + b) * c) + (d / e)"
#expresion = "x * (y + z) - (w / v) + u"
expresion = "a * (b + c) - (d * e) / f"
#expresion = "a / b * c / d"
#expresion = "(a + b * c - (d / e + f) * g) / h"
#expresion = "(a + (b * (c + (d - e)))) / f"
#expresion = "(a - 8) + 7 * 16/4 + 13"
codigo = generar_codigo_intermedio(expresion)
print("\nCódigo intermedio:")
for instruccion in codigo:
    print(instruccion)