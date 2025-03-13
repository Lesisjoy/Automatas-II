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
    
    # Convertir la expresión infija a postfija
    postfijo = infijo_a_postfijo(expresion)
    
    # Convertir la expresión infija a prefija
    prefijo = infijo_a_prefijo(expresion)
    
    # Generar el código intermedio
    codigo_intermedio = postfijo_a_codigo_intermedio(postfijo)
    
    return postfijo, prefijo, codigo_intermedio

# Menú mejorado con opción para imprimir todo
def menu():
    expresion = input("Ingrese la expresión infija: ")
    postfijo, prefijo, codigo_intermedio = generar_codigo_intermedio(expresion)
    
    while True:
        print("\nSeleccione una opción:")
        print("1. Mostrar notación postfija")
        print("2. Mostrar notación prefija")
        print("3. Mostrar código intermedio")
        print("4. Mostrar todo")
        print("5. Salir")
        
        opcion = input("Opción: ")
        
        if opcion == '1':
            print("\n🔹 Notación postfija:", ' '.join(postfijo))
        elif opcion == '2':
            print("\n🔹 Notación prefija:", ' '.join(prefijo))
        elif opcion == '3':
            print("\n📌 Código Intermedio:")
            for instruccion in codigo_intermedio:
                print(instruccion)
        elif opcion == '4':
            print("\nExpresion Ingresa:", ' '.join(expresion))
            print("📌 Notaciones:")
            print("\nNotación prefija:", ' '.join(prefijo))
            print("Notación postfija:", ' '.join(postfijo))
            print("\n📌 Código Intermedio:")
            for instruccion in codigo_intermedio:
                print(instruccion)
        elif opcion == '5':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecutar el menú
menu()

