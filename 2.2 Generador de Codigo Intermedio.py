import re
import math
import os
from lexer import tokens 

# Funciones y variables permitidas
funciones_permitidas = {'sin', 'cos', 'tan', 'ln', 'sqrt'}
variables_permitidas = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

# MANEJO DE ERRORES #
def verificar_errores(expresion):
    """
    Verifica errores comunes en una expresión matemática.
    
    :param expresion: Expresión en notación infija.
    :raises ValueError: Si se encuentra un error en la expresión.
    """
    # Verificar expresiones vacías
    if not expresion.strip():
        raise ValueError("Expresión vacía")

    # Verificar paréntesis balanceados
    pila = []
    for caracter in expresion:
        if caracter == '(':
            pila.append(caracter)
        elif caracter == ')':
            if not pila or pila[-1] != '(':
                raise ValueError("Paréntesis no balanceados")
            pila.pop()
    if pila:
        raise ValueError("Paréntesis no balanceados")
    
     # Verificar si la expresión solo contiene un número, una letra o una función matemática sin operadores
    if re.fullmatch(r'\s*[a-zA-Z]+\s*', expresion):  # Solo una letra
        raise ValueError("Expresión inválida: falta un operador")
    if re.fullmatch(r'\s*\d+(\.\d+)?\s*', expresion):  # Solo un número
        raise ValueError("Expresión inválida: falta un operador")
    if re.fullmatch(r'\s*(' + '|'.join(funciones_permitidas) + r')\s*\(\s*[a-zA-Z0-9]*\s*\)\s*', expresion):  # Función matemática sin operadores
        raise ValueError("Expresión inválida: falta un operador")

    # Verificar operadores faltantes o mal colocados
    operadores = {'+', '-', '*', '/', '%', '^'}
    for i in range(len(expresion) - 1):
        if expresion[i] in operadores and expresion[i + 1] in operadores:
            raise ValueError("Operadores consecutivos no permitidos")

    # Verificar división por cero
    if '/ 0' in expresion or '% 0' in expresion:
        raise ValueError("División por cero no permitida")

    # Verificar caracteres no permitidos
    caracteres_permitidos = set("0123456789+-*/%()^ .abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for caracter in expresion:
        if caracter not in caracteres_permitidos:
            raise ValueError(f"Carácter no permitido: '{caracter}'")

    # Verificar funciones no definidas
    for func in re.findall(r'\b[a-zA-Z_]+\b', expresion):
        if func in funciones_permitidas:
            continue  # Es una función permitida
        elif func in variables_permitidas:
            continue  # Es una variable permitida
        else:
            raise ValueError(f"Función o variable no definida: '{func}'")

    # Verificar funciones sin argumentos
    for func in funciones_permitidas:
        if re.search(fr'{func}\s*\(\s*\)', expresion):
            raise ValueError(f"Función '{func}' sin argumentos")

    # Verificar paréntesis vacíos
    if re.search(r'\(\s*\)', expresion):
        raise ValueError("Paréntesis vacíos")

    # Verificar expresiones incompletas
    if expresion.strip().endswith(('+', '-', '*', '/', '%', '^', '(')):
        raise ValueError("Expresión incompleta")

    # Verificar números mal formados
    if re.search(r'\d+\.\d+\.', expresion):  
        raise ValueError("Número mal formado: múltiples puntos decimales")

    for numero in re.findall(r'\b\d+(\.\d+)?\b', expresion):
        try:
            float(numero)  # Intenta convertir a float
        except ValueError:
            raise ValueError(f"Número mal formado: '{numero}'")


# CONVERSIÓN DE NOTACIONES #
def infijo_a_postfijo(expresion):
    """
    Convierte una expresión infija en notación postfija.
    
    :param expresion: Expresión infija como cadena de texto.
    :return: Lista de tokens en notación postfija.
    :raises ValueError: Si hay un error en la conversión.
    """
    try:
        precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3}
        
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
                    while i < len(expresion) and (expresion[i].isdigit() or expresion[i] == '.'):
                        num += expresion[i]
                        i += 1
                    salida.append(num)
                    continue
                else:
                    # Es una variable o función
                    var = ''
                    while i < len(expresion) and (expresion[i].isalpha() or expresion[i] == '_'):
                        var += expresion[i]
                        i += 1
                    if var in funciones_permitidas:
                        pila.append(var)
                    else:
                        salida.append(var)
                    continue
            i += 1
        while pila:
            salida.append(pila.pop())
        return salida
    except Exception as e:
        raise ValueError(f"Error en conversión a postfijo: {e}")

def infijo_a_prefijo(expresion):
    """
    Convierte una expresión infija en notación prefija.
    
    :param expresion: Expresión infija como cadena de texto.
    :return: Lista de tokens en notación prefija.
    :raises ValueError: Si hay un error en la conversión.
    """
    try:
        precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3}
        
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
                    while i < len(expresion) and (expresion[i].isdigit() or expresion[i] == '.'):
                        num += expresion[i]
                        i += 1
                    salida.append(num[::-1])  # Invertir el número para restaurar su orden original
                    continue
                else:
                    # Es una variable o función
                    var = ''
                    while i < len(expresion) and (expresion[i].isalpha() or expresion[i] == '_'):
                        var += expresion[i]
                        i += 1
                    if var[::-1] in funciones_permitidas:
                        pila.append(var[::-1])
                    else:
                        salida.append(var[::-1])  # Invertir la variable para restaurar su orden original
                    continue
            i += 1
        while pila:
            salida.append(pila.pop())
        return salida[::-1]  # Invertir la salida para obtener la notación prefija
    except Exception as e:
        raise ValueError(f"Error en conversión a prefijo: {e}")

def infijo_a_codigo_p(expresion):
    """
    Convierte una expresión infija en código P.
    
    :param expresion: Expresión infija como cadena de texto.
    :return: Código P como cadena de texto.
    :raises ValueError: Si hay un error en la conversión.
    """
    try:
        # Precedencia de los operadores
        precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3}
        
        # Mapeo de operadores a sus equivalentes en código P
        operadores_p = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
            '%': 'MOD',
            '^': 'POW',
            'sin': 'SIN',
            'cos': 'COS',
            'tan': 'TAN',
            'ln': 'LN',
            'sqrt': 'SQRT'
        }
        
        # Función para verificar si un carácter es un operador
        def es_operador(caracter):
            return caracter in precedencia
        
        # Pila para operadores y salida para el código P
        pila_operadores = []
        codigo_p = []
        
        i = 0
        while i < len(expresion):
            caracter = expresion[i]
            
            # Ignorar espacios en blanco
            if caracter == ' ':
                i += 1
                continue
            
            # Si es un paréntesis de apertura, lo agregamos a la pila
            if caracter == '(':
                pila_operadores.append(caracter)
            
            # Si es un paréntesis de cierre, procesamos los operadores hasta encontrar el de apertura
            elif caracter == ')':
                while pila_operadores and pila_operadores[-1] != '(':
                    codigo_p.append(operadores_p[pila_operadores.pop()])
                pila_operadores.pop()  # Eliminar el '(' de la pila
            
            # Si es un operador, procesamos los operadores de mayor o igual precedencia
            elif es_operador(caracter):
                while (pila_operadores and pila_operadores[-1] != '(' and
                       precedencia[pila_operadores[-1]] >= precedencia[caracter]):
                    codigo_p.append(operadores_p[pila_operadores.pop()])
                pila_operadores.append(caracter)
            
            # Si es una función, la agregamos a la pila
            elif caracter.isalpha():
                func = ''
                while i < len(expresion) and (expresion[i].isalpha() or expresion[i] == '_'):
                    func += expresion[i]
                    i += 1
                if func in funciones_permitidas:
                    pila_operadores.append(func)
                else:
                    codigo_p.append(f"PUSH {func}")
                continue
            
            # Si es un operando (número), lo agregamos directamente al código P
            else:
                if caracter.isdigit():
                    num = ''
                    while i < len(expresion) and (expresion[i].isdigit() or expresion[i] == '.'):
                        num += expresion[i]
                        i += 1
                    codigo_p.append(f"PUSH {num}")
                    continue
            
            i += 1
        
        # Procesar los operadores restantes en la pila
        while pila_operadores:
            codigo_p.append(operadores_p[pila_operadores.pop()])
        
        # Unir el código P en una sola cadena con saltos de línea
        return "\n".join(codigo_p)
    except Exception as e:
        raise ValueError(f"Error en conversión a código P: {e}")

def postfijo_a_codigo_intermedio(postfijo):
    """
    Convierte una expresión en notación postfija a código intermedio y código P.
    
    :param postfijo: Lista de tokens en notación postfija.
    :return: Una tupla con el código intermedio y el código P.
    :raises ValueError: Si hay un error en la conversión.
    """
    try:
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
            '^': 'POW',
            'sin': 'SIN',
            'cos': 'COS',
            'tan': 'TAN',
            'ln': 'LN',
            'sqrt': 'SQRT'
        }

        temp_counter = 0
        def nueva_temp():
            nonlocal temp_counter
            temp = f'T{temp_counter}'
            temp_counter += 1
            return temp

        for token in postfijo:
            if token in operadores_p:  # Es un operador o función
                if token in {'sin', 'cos', 'tan', 'ln', 'sqrt'}:  # Es una función
                    if len(pila) < 1:
                        raise ValueError("Expresión inválida: no hay suficientes operandos para la función.")
                    operando = pila.pop()
                    
                    # Generar código intermedio
                    temp = nueva_temp()
                    codigo_intermedio.append(f'{temp} = {token}({operando})')
                    pila.append(temp)
                    
                    # Generar código P
                    codigo_p.append(f"PUSH {operando}")
                    codigo_p.append(operadores_p[token])
                else:  # Es un operador binario
                    if len(pila) < 2:
                        raise ValueError("Expresión inválida: no hay suficientes operandos para el operador.")
                    operando2 = pila.pop()
                    operando1 = pila.pop()
                    
                    # Generar código intermedio
                    temp = nueva_temp()
                    codigo_intermedio.append(f'{temp} = {operando1} {token} {operando2}')
                    pila.append(temp)
                    
                    # Generar código P
                    codigo_p.append(f"PUSH {operando1}")
                    codigo_p.append(f"PUSH {operando2}")
                    codigo_p.append(operadores_p[token])
            else:  # Es un operando (número o variable)
                pila.append(token)
        
        if len(pila) != 1:
            raise ValueError("Expresión inválida: la pila no se redujo a un solo valor.")
        
        # Agregar la asignación final (Z = resultado)
        resultado_final = pila.pop()
        codigo_intermedio.append(f'Z = {resultado_final}')
        
        # Devolver el código intermedio y el código P
        return codigo_intermedio, "\n".join(codigo_p)
    except Exception as e:
        raise ValueError(f"Error en conversión a código intermedio: {e}")

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
            triplos.append(f"({i+1}, {partes[3]}, {partes[2]}, {partes[4]})")  # Formato: (número, operador, operando1, operando2)
        elif len(partes) == 3:  # Formato: Z = operando
            triplos.append(f"({i+1}, =, {partes[2]}, Z)")  # Formato: (número, operador, operando1, operando2)
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
            cuadruplos.append(f"({i+1}, {partes[3]}, {partes[2]}, {partes[4]}, {partes[0]})")  # Formato: (número, operador, operando1, operando2, resultado)
        elif len(partes) == 3:  # Formato: Z = operando
            cuadruplos.append(f"({i+1}, =, {partes[2]}, , Z)")  # Formato: (número, operador, operando1, operando2, resultado)
    return cuadruplos

def cargar_expresiones_desde_archivo(ruta_archivo):
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
        # Verificar errores antes de procesar
        verificar_errores(expresion)
        
        postfijo = infijo_a_postfijo(expresion)
        prefijo = infijo_a_prefijo(expresion)
        codigo_intermedio, codigo_p_intermedio = postfijo_a_codigo_intermedio(postfijo)
        codigo_p_directo = infijo_a_codigo_p(expresion)
        triplos = generar_triplos(codigo_intermedio)
        cuadruplos = generar_cuadruplos(codigo_intermedio)
        
        resultados = [f"\n----- Expresión {numero_expresion}: {expresion} -----"]
        
        if opcion == '1' or opcion == '5':
            resultados.append("\n📌 Notaciones:")
            resultados.append(f"🔹 Prefija: {' '.join(prefijo)}")
            resultados.append(f"🔹 Postfija: {' '.join(postfijo)}")
            resultados.append("\n📌 Código Intermedio:")
            for instruccion in codigo_intermedio:
                resultados.append(instruccion)
        
        if opcion == '2' or opcion == '5':
            resultados.append("\n📌 Código P (desde código intermedio):")
            resultados.append(codigo_p_intermedio)
            resultados.append("\n📌 Código P (directo desde infijo):")
            resultados.append(codigo_p_directo)
        
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

def guardar_resultados(ruta_salida, resultados):
    """
    Guarda los resultados en un archivo.
    
    :param ruta_salida: Ruta del archivo de salida.
    :param resultados: Lista de resultados a guardar.
    """
    try:
        with open(ruta_salida, "w", encoding="utf-8") as archivo:
            for resultado in resultados:
                archivo.write(str(resultado) + "\n")
        print(f"✅ Resultados guardados en '{ruta_salida}'.")
    except IOError as e:
        print(f"❌ Error al guardar resultados: {e}")

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
        guardar_resultados(ruta_salida, resultados_totales)

        # Abrir automáticamente el archivo de resultados
        print(f"📂 Abriendo archivo: {ruta_salida}")
        os.system(f'start {ruta_salida}')  # Para Windows
        # os.system(f'xdg-open {ruta_salida}')  # Para Linux
        # os.system(f'open {ruta_salida}')  # Para MacOS

if __name__ == "__main__":
    main()