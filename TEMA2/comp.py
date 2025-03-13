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
                if caracter.isdigit():
                    num = ''
                    while i < len(expresion) and expresion[i].isdigit():
                        num += expresion[i]
                        i += 1
                    salida.append(num)
                    continue
                else:
                    # Manejar variables de múltiples caracteres
                    var = ''
                    while i < len(expresion) and (expresion[i].isalpha() or expresion[i].isdigit()):
                        var += expresion[i]
                        i += 1
                    salida.append(var)
                    continue
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
                if len(pila) < 2:
                    raise ValueError("Expresión inválida: no hay suficientes operandos para el operador.")
                operando2 = pila.pop()
                operando1 = pila.pop()
                temp = nueva_temp()
                codigo_intermedio.append(f'{temp} = {operando1} {token} {operando2}')
                pila.append(temp)
            else:
                pila.append(token)
        if len(pila) != 1:
            raise ValueError("Expresión inválida: la pila no se redujo a un solo valor.")
        codigo_intermedio.append(f'Z = {pila.pop()}')
        return codigo_intermedio
    
    # Convertir la expresión infija a postfija
    postfijo = infijo_a_postfijo(expresion)
    
    # Convertir la expresión infija a prefija
    prefijo = infijo_a_prefijo(expresion)
    
    # Generar el código intermedio
    codigo_intermedio = postfijo_a_codigo_intermedio(postfijo)
    
    return postfijo, prefijo, codigo_intermedio


def validar_expresion(expresion):
    caracteres_validos = set("0123456789+-*/%() ")
    if not expresion:
        raise ValueError("La expresión está vacía.")
    if not all(caracter in caracteres_validos for caracter in expresion):
        raise ValueError("La expresión contiene caracteres no válidos.")
    # Verificar paréntesis balanceados
    pila = []
    for caracter in expresion:
        if caracter == '(':
            pila.append(caracter)
        elif caracter == ')':
            if not pila:
                raise ValueError("Paréntesis desbalanceados.")
            pila.pop()
    if pila:
        raise ValueError("Paréntesis desbalanceados.")

# Menú
def menu():
    while True:
        expresion = input("Ingrese la expresión infija (o 'salir' para terminar): ")
        if expresion.lower() == 'salir':
            print("Saliendo...")
            break
        try:
            validar_expresion(expresion)
            postfijo, prefijo, codigo_intermedio = generar_codigo_intermedio(expresion)
        except ValueError as e:
            print(f"Error: {e}")
            continue
        
        while True:
            print("\nSeleccione una opción para imprimir:")
            print("1. Notación postfija")
            print("2. Notación prefija")
            print("3. Código intermedio")
            print("4. Ingresar nueva expresión")
            opcion = input("Opción: ")
            
            if opcion == '1':
                print("\nNotación postfija:", ' '.join(postfijo))
            elif opcion == '2':
                print("\nNotación prefija:", ' '.join(prefijo))
            elif opcion == '3':
                print("\nCódigo intermedio:")
                for instruccion in codigo_intermedio:
                    print(instruccion)
            elif opcion == '4':
                break
            else:
                print("Opción no válida. Intente de nuevo.")
menu()