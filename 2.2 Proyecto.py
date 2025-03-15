def infijo_a_postfijo(expresion):
    """
    Convierte una expresión infija en notación postfija.
    
    :param expresion: Expresión infija como cadena de texto.
    :return: Lista de tokens en notación postfija.
    """
    precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
    
    def es_operador(caracter):
        return caracter in precedencia
    
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
                salida.append(caracter)
        i += 1
    while pila:
        salida.append(pila.pop())
    return salida


def infijo_a_prefijo(expresion):
    """
    Convierte una expresión infija en notación prefija.
    
    :param expresion: Expresión infija como cadena de texto.
    :return: Lista de tokens en notación prefija.
    """
    precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
    
    def es_operador(caracter):
        return caracter in precedencia
    
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


def postfijo_a_codigo_intermedio(postfijo):
    """
    Convierte una expresión en notación postfija a código intermedio y código P.
    
    :param postfijo: Lista de tokens en notación postfija.
    :return: Una tupla con el código intermedio y el código P.
    """
    pila = []
    codigo_intermedio = []
    codigo_p = []  # Código P generado

    # Mapeo de operadores a sus equivalentes en código P
    operadores_p = {
        '+': 'ADD',
        '-': 'SUB',
        '*': 'MUL',
        '/': 'DIV',
        '%': 'MOD',
        '^': 'POW'
    }

    temp_counter = 0
    def nueva_temp():
        nonlocal temp_counter
        temp = f'T{temp_counter}'
        temp_counter += 1
        return temp

    for token in postfijo:
        if token in operadores_p:  # Es un operador
            if len(pila) < 2:
                raise ValueError("Expresión inválida: no hay suficientes operandos para el operador.")
            operando2 = pila.pop()
            operando1 = pila.pop()
            
            # Generar código intermedio
            temp = nueva_temp()
            codigo_intermedio.append(f'{temp} = {operando1} {token} {operando2}')
            pila.append(temp)
            
            # Generar código P
            # Usamos los operandos originales en lugar de las temporales
            if operando1.startswith('T'):
                # Si es una temporal, buscamos su definición en el código intermedio
                for instruccion in codigo_intermedio:
                    if instruccion.startswith(operando1):
                        partes = instruccion.split()
                        operando1_real = f"{partes[2]} {partes[3]} {partes[4]}"
                        break
            else:
                operando1_real = operando1

            if operando2.startswith('T'):
                # Si es una temporal, buscamos su definición en el código intermedio
                for instruccion in codigo_intermedio:
                    if instruccion.startswith(operando2):
                        partes = instruccion.split()
                        operando2_real = f"{partes[2]} {partes[3]} {partes[4]}"
                        break
            else:
                operando2_real = operando2

            # Generar código P
            codigo_p.append(f"PUSH {operando1_real}")
            codigo_p.append(f"PUSH {operando2_real}")
            codigo_p.append(operadores_p[token])
        else:  # Es un operando (número o variable)
            pila.append(token)
            # No hacemos PUSH aquí, solo cuando se use en una operación
    
    if len(pila) != 1:
        raise ValueError("Expresión inválida: la pila no se redujo a un solo valor.")
    
    # Agregar la asignación final (Z = resultado)
    resultado_final = pila.pop()
    codigo_intermedio.append(f'Z = {resultado_final}')
    
    # Devolver el código intermedio y el código P
    return codigo_intermedio, "\n".join(codigo_p)


def generar_triplos(codigo_intermedio):
    """
    Genera triplos a partir del código intermedio.
    
    :param codigo_intermedio: Lista de instrucciones de código intermedio.
    :return: Lista de triplos.
    """
    triplos = []
    for i, instruccion in enumerate(codigo_intermedio):
        partes = instruccion.split()
        if len(partes) == 5:  # Formato: temp = operando1 operador operando2
            triplos.append(f"({i+1}, {partes[2]}, {partes[3]}, {partes[4]})")
        elif len(partes) == 3:  # Formato: Z = operando
            triplos.append(f"({i+1}, =, {partes[2]}, Z)")
    return triplos


def generar_cuadruplos(codigo_intermedio):
    """
    Genera cuádruplos a partir del código intermedio.
    
    :param codigo_intermedio: Lista de instrucciones de código intermedio.
    :return: Lista de cuádruplos.
    """
    cuadruplos = []
    for i, instruccion in enumerate(codigo_intermedio):
        partes = instruccion.split()
        if len(partes) == 5:  # Formato: temp = operando1 operador operando2
            cuadruplos.append(f"({i+1}, {partes[2]}, {partes[3]}, {partes[4]}, {partes[0]})")
        elif len(partes) == 3:  # Formato: Z = operando
            cuadruplos.append(f"({i+1}, =, {partes[2]}, Z, -)")
    return cuadruplos


def generar_codigo_intermedio(expresion):
    """
    Convierte una expresión infija en notación postfija y prefija, y genera código intermedio y código P.
    
    :param expresion: Expresión infija como cadena de texto.
    :return: Una tupla con la notación postfija, prefija, código intermedio, código P, triplos y cuádruplos.
    """
    # Convertir la expresión infija a postfija
    postfijo = infijo_a_postfijo(expresion)
    
    # Convertir la expresión infija a prefija
    prefijo = infijo_a_prefijo(expresion)
    
    # Generar el código intermedio y el código P
    codigo_intermedio, codigo_p = postfijo_a_codigo_intermedio(postfijo)
    
    # Generar triplos y cuádruplos
    triplos = generar_triplos(codigo_intermedio)
    cuadruplos = generar_cuadruplos(codigo_intermedio)
    
    return postfijo, prefijo, codigo_intermedio, codigo_p, triplos, cuadruplos


def cargar_expresiones_desde_archivo(ruta_archivo):
    """
    Carga expresiones matemáticas desde un archivo.
    
    :param ruta_archivo: Ruta del archivo que contiene las expresiones.
    :return: Lista de expresiones.
    """
    expresiones = []
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea and not linea.startswith("#"):  # Ignorar líneas vacías y comentarios
                    expresiones.append(linea)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{ruta_archivo}'.")
    return expresiones


def mostrar_menu():
    """
    Muestra el menú de opciones al usuario.
    """
    print("\nSeleccione una opción:")
    print("1. Notaciones (prefija, postfija y código intermedio)")
    print("2. Código P (código intermedio)")
    print("3. Triplos")
    print("4. Cuádruplos")
    print("5. Todas las anteriores")
    print("6. Salir")


def procesar_expresion(expresion, opcion, numero_expresion):
    """
    Procesa una expresión y devuelve los resultados según la opción seleccionada.
    
    :param expresion: Expresión en notación infija.
    :param opcion: Opción seleccionada por el usuario.
    :param numero_expresion: Número de la expresión (para etiquetar los resultados).
    :return: Lista de resultados.
    """
    try:
        postfijo, prefijo, codigo_intermedio, codigo_p, triplos, cuadruplos = generar_codigo_intermedio(expresion)
        resultados = [f"\n----- Expresión {numero_expresion}: {expresion} -----"]
        
        if opcion == '1' or opcion == '5':
            resultados.append("\n📌 Notaciones:")
            resultados.append(f"🔹 Prefija: {' '.join(prefijo)}")
            resultados.append(f"🔹 Postfija: {' '.join(postfijo)}")
            resultados.append("\n📌 Código Intermedio:")
            for instruccion in codigo_intermedio:
                resultados.append(instruccion)
        
        if opcion == '2' or opcion == '5':
            resultados.append("\n📌 Código P:")
            resultados.append(codigo_p)
        
        if opcion == '3' or opcion == '5':
            resultados.append("\n📌 Triplos:")
            for triplo in triplos:
                resultados.append(triplo)
        
        if opcion == '4' or opcion == '5':
            resultados.append("\n📌 Cuádruplos:")
            for cuadruplo in cuadruplos:
                resultados.append(cuadruplo)
        
        resultados.append("")  # Línea en blanco para separar expresiones
        return resultados
    except ValueError as e:
        return [f"\n----- Expresión {numero_expresion}: {expresion} -----",
                f"❌ Error al procesar la expresión: {e}"]


def main():
    # Cargar expresiones desde el archivo
    ruta_entrada = "datos.txt"
    expresiones = cargar_expresiones_desde_archivo(ruta_entrada)
    
    if not expresiones:
        print("No hay expresiones para procesar.")
        return
    
    # Mostrar el menú
    while True:
        mostrar_menu()
        opcion = input("Opción: ")
        
        if opcion == '6':
            print("Saliendo...")
            break
        elif opcion not in ['1', '2', '3', '4', '5']:
            print("❌ Opción no válida. Intente de nuevo.")
            continue
        
        # Procesar todas las expresiones
        resultados_totales = []
        for i, expresion in enumerate(expresiones, 1):
            resultados = procesar_expresion(expresion, opcion, i)
            resultados_totales.extend(resultados)
        
        # Guardar resultados en un archivo
        ruta_salida = "resultados.txt"
        with open(ruta_salida, "w", encoding="utf-8") as archivo:
            for resultado in resultados_totales:
                archivo.write(resultado + "\n")
        
        # Solo imprimir el mensaje de confirmación
        print(f"✅ Resultados guardados en '{ruta_salida}'.")


if __name__ == "__main__":
    main()