import ply.yacc as yacc
import math
import random
import re
from lexer import tokens


# MANEJO DE ERORES #
def verificar_errores(expresion):
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

    # Verificar operadores faltantes o mal colocados
    operadores = ['+', '-', '*', '/', '%']
    for i in range(len(expresion) - 1):
        if expresion[i] in operadores and expresion[i + 1] in operadores:
            raise ValueError("Operadores consecutivos no permitidos")

    # Verificar división por cero
    if '/ 0' in expresion or '% 0' in expresion:
        raise ValueError("División por cero no permitida")

    # Verificar caracteres no permitidos
    caracteres_permitidos = set("0123456789+-*/%()^ ")
    for caracter in expresion:
        if caracter not in caracteres_permitidos:
            raise ValueError(f"Carácter no permitido: '{caracter}'")

def infijo_a_postfijo(expresion):
    """
    Convierte una expresión infija en notación postfija.
    
    :param expresion: Expresión infija como cadena de texto.
    :return: Lista de tokens en notación postfija.
    """
    try:

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
    except Exception as e:
        raise ValueError(f"Error en conversion a posfijo: {e}")

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

def infijo_a_codigo_p(expresion):
    """
    Convierte una expresión infija en código P.
    
    :param expresion: Expresión infija como cadena de texto.
    :return: Código P como cadena de texto.
    """
    # Precedencia de los operadores
    precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
    
    # Mapeo de operadores a sus equivalentes en código P
    operadores_p = {
        '+': 'ADD',
        '-': 'SUB',
        '*': 'MUL',
        '/': 'DIV',
        '%': 'MOD'
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
        
        # Si es un operando (número o variable), lo agregamos directamente al código P
        else:
            # Manejar números de más de un dígito
            if caracter.isdigit():
                num = ''
                while i < len(expresion) and expresion[i].isdigit():
                    num += expresion[i]
                    i += 1
                codigo_p.append(f"PUSH {num}")
                continue
            else:
                codigo_p.append(f"PUSH {caracter}")
        
        i += 1
    
    # Procesar los operadores restantes en la pila
    while pila_operadores:
        codigo_p.append(operadores_p[pila_operadores.pop()])
    
    # Unir el código P en una sola cadena con saltos de línea
    return "\n".join(codigo_p)



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
                archivo.write(str(resultado) + "\n")  # Convertir a cadena si no lo es
        
        # Solo imprimir el mensaje de confirmación
        print(f"\n✅ Resultados guardados en '{ruta_salida}'.")


if __name__ == "__main__":
    main()