class GeneradorCodigo:
    def __init__(self):
        self.codigo = []  # Lista donde almacenaremos el código ensamblador generado
        self.variables = {}  # Diccionario para almacenar variables y sus valores

    def cargar_variables(self, archivo):
        """Carga variables desde el archivo datos2.txt"""
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if "=" in linea:
                        nombre, valor = map(str.strip, linea.split("=", 1))
                        if valor.isdigit():
                            self.variables[nombre] = int(valor)
                        elif valor.replace(".", "", 1).isdigit():
                            self.variables[nombre] = float(valor)
                        else:
                            self.variables[nombre] = valor  # Guardar como string
        except FileNotFoundError:
            print("❌ Error: No se encontró el archivo.")

    def generar(self, expresion):
        """Convierte una expresión matemática a código ensamblador."""
        self.codigo = []  # Limpiar código previo
        tokens = expresion.replace("(", " ( ").replace(")", " ) ").split()
        self.pila_operadores = []  # Pila de operadores
        self.pila_operandos = []   # Pila de operandos (valores)
        self.procesar_expresion(tokens)
        return "\n".join(self.codigo)  # Devolver código ensamblador generado

    def procesar_expresion(self, tokens):
        precedencia = {'+': 1, '-': 1, '*': 2, '/': 2}  # Prioridad de operadores
        for token in tokens:
            if token.isdigit():  # Si es un número entero
                self.codigo.append(f"PUSH {token}")
                self.pila_operandos.append(token)
            elif token.replace(".", "", 1).isdigit():  # Si es un número decimal
                self.codigo.append(f"PUSH {token}")
                self.pila_operandos.append(token)
            elif token in self.variables:  # Si es una variable
                valor = self.variables[token]
                self.codigo.append(f"PUSH {valor}")
                self.pila_operandos.append(str(valor))
            elif token in precedencia:  # Si es un operador
                while (self.pila_operadores and self.pila_operadores[-1] in precedencia and
                       precedencia[self.pila_operadores[-1]] >= precedencia[token]):
                    self.evaluar_operador()
                self.pila_operadores.append(token)
            elif token == '(':  # Si es un paréntesis de apertura
                self.pila_operadores.append(token)
            elif token == ')':  # Si es un paréntesis de cierre
                while self.pila_operadores and self.pila_operadores[-1] != '(':
                    self.evaluar_operador()
                self.pila_operadores.pop()  # Eliminar '(' de la pila

        while self.pila_operadores:  # Procesar operadores restantes
            self.evaluar_operador()

    def evaluar_operador(self):
        if len(self.pila_operandos) < 2:  # Evitar errores de pila
            return

        operador = self.pila_operadores.pop()
        b = self.pila_operandos.pop()
        a = self.pila_operandos.pop()
        
        if operador == '+':
            self.codigo.append("ADD")
        elif operador == '-':
            self.codigo.append("SUB")
        elif operador == '*':
            self.codigo.append("MUL")
        elif operador == '/':
            self.codigo.append("DIV")

        self.pila_operandos.append(f"({a} {operador} {b})")  # Agregar resultado parcial


# 📌 Leer variables y expresiones desde datos2.txt
generador = GeneradorCodigo()
generador.cargar_variables("datos3.txt")

# 📌 Leer expresiones matemáticas del archivo
try:
    with open("datos3.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if "=" in linea:
                continue  # Omitir declaraciones de variables
            
            print(f"\nExpresión: {linea}")
            print(generador.generar(linea))

except FileNotFoundError:
    print("❌ Error: No se encontró el archivo 'datos3.txt'.")
