class GeneradorCodigo:
    def __init__(self):
        self.codigo = []  # Código ensamblador generado
        self.variables = {}  # Variables almacenadas

        # Mapeo de operadores y funciones entre formatos
        self.operadores = {
            "+": "SUMITA", "-": "RESTA", "*": "MULTIPLICA", "/": "DIVIDE",
            "^": "POTENCIA", "%": "MODULO"
        }
        self.funciones = {
            "sqrt": "RAIZ", "sin": "SENO", "cos": "COSENO", "tan": "TANGENTE",
            "log": "LOGARITMO_10"
        }

    def cargar_variables(self, archivo):
        """Carga variables desde el archivo datos2.txt"""
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea or linea.startswith("#"):  # Ignorar comentarios y líneas vacías
                        continue
                    if "=" in linea:  # Guardar variables
                        nombre, valor = map(str.strip, linea.split("=", 1))
                        if valor.isdigit():
                            self.variables[nombre] = int(valor)
                        elif valor.replace(".", "", 1).isdigit():
                            self.variables[nombre] = float(valor)
                        else:
                            self.variables[nombre] = valor
        except FileNotFoundError:
            print("❌ Error: No se encontró el archivo.")

    def generar(self, expresion):
        """Convierte una expresión matemática a código ensamblador."""
        self.codigo = []  # Limpiar código previo

        # Reemplazar operadores estándar con los equivalentes en palabras reservadas
        for operador, reemplazo in self.operadores.items():
            expresion = expresion.replace(operador, f" {reemplazo} ")

        # Reemplazar funciones matemáticas estándar con sus equivalentes en palabras reservadas
        for funcion, reemplazo in self.funciones.items():
            expresion = expresion.replace(funcion + "(", reemplazo + " (")

        tokens = expresion.replace("(", " ( ").replace(")", " ) ").split()
        self.pila_operadores = []  # Pila de operadores
        self.pila_operandos = []   # Pila de operandos (valores)
        self.procesar_expresion(tokens)
        return "\n".join(self.codigo)  # Devolver código ensamblador generado

    def procesar_expresion(self, tokens):
        precedencia = {
            'SUMITA': 1, 'RESTA': 1, 'MULTIPLICA': 2, 'DIVIDE': 2, 'MODULO': 2,
            'POTENCIA': 3, 'RAIZ': 4, 'SENO': 4, 'COSENO': 4, 'TANGENTE': 4,
            'LOGARITMO_NATURAL': 4, 'LOGARITMO_10': 4, 'ELEVADO': 3, 'ALEATORIO': 5
        }  # Prioridad de operadores
        
        for token in tokens:
            if token.isdigit():  # Número entero
                self.codigo.append(f"PUSH {token}")
                self.pila_operandos.append(token)
            elif token.replace(".", "", 1).isdigit():  # Número decimal
                self.codigo.append(f"PUSH {token}")
                self.pila_operandos.append(token)
            elif token in self.variables:  # Variable declarada
                valor = self.variables[token]
                self.codigo.append(f"PUSH {valor}")
                self.pila_operandos.append(str(valor))
            elif token in precedencia:  # Operador
                while (self.pila_operadores and self.pila_operadores[-1] in precedencia and
                    precedencia[self.pila_operadores[-1]] >= precedencia[token]):
                    self.evaluar_operador()
                self.pila_operadores.append(token)
            elif token == '(':  # Paréntesis de apertura
                self.pila_operadores.append(token)
            elif token == ')':  # Paréntesis de cierre
                while self.pila_operadores and self.pila_operadores[-1] != '(':
                    self.evaluar_operador()
                self.pila_operadores.pop()  # Eliminar '(' de la pila

        while self.pila_operadores:  # Procesar operadores restantes
            self.evaluar_operador()

    def evaluar_operador(self):
        operador = self.pila_operadores.pop()

        # Operadores unarios (funciones matemáticas)
        if operador in {"RAIZ", "SENO", "COSENO", "TANGENTE", "LOGARITMO_10"}:
            if len(self.pila_operandos) < 1:
                return
            a = self.pila_operandos.pop()
            
            if operador == "RAIZ":
                self.codigo.append("SQRT")
                self.codigo.append("SQRT")  # Procede con la operación de raíz cuadrada
            elif operador == "SENO":
                self.codigo.append("SIN")
            elif operador == "COSENO":
                self.codigo.append("COS")
            elif operador == "TANGENTE":
                self.codigo.append("TAN")
            elif operador == "LOGARITMO_10":
                self.codigo.append("LOG10")

            self.pila_operandos.append(f"{operador}({a})")  # Registra el operando con su función
            return

        # Operadores binarios
        if len(self.pila_operandos) < 2:
            return
        b = self.pila_operandos.pop()
        a = self.pila_operandos.pop()
        
        if operador == 'SUMITA':
            self.codigo.append("ADD")
        elif operador == 'RESTA':
            self.codigo.append("SUB")
        elif operador == 'MULTIPLICA':
            self.codigo.append("MUL")
        elif operador == 'DIVIDE':
            if b == '0':  # Verifica si el divisor es 0
                print("❌ Error: División por cero detectada.")
                return
            self.codigo.append("DIV")
        elif operador == 'MODULO':
            self.codigo.append("MOD")
        elif operador == 'POTENCIA':
            self.codigo.append("POW")

        self.pila_operandos.append(f"({a} {operador} {b})")  # Agregar resultado parcial

# 📌 Leer variables y expresiones desde datos3.txt
generador = GeneradorCodigo()
generador.cargar_variables("datos3.txt")

# 📌 Leer expresiones matemáticas del archivo
try:
    with open("datos3.txt", "r", encoding="utf-8") as archivo:
        print("\n📌 Generar codigo emsamblador:")
        for linea in archivo:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" in linea:
                continue  # Omitir comentarios, líneas vacías y declaraciones de variables
            
            print(f"\nExpresión: {linea}")
            print(generador.generar(linea))

except FileNotFoundError:
    print("❌ Error: No se encontró el archivo 'datos3.txt'.")