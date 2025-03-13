class GeneradorCodigoP:
    def __init__(self):
        self.codigo_p = []  # Código P generado
        self.variables = {}  # Variables almacenadas

        # Mapeo de operadores y funciones
        self.operadores = {
            "+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV",
            "^": "POW", "%": "MOD"
        }
        self.funciones = {
            "sqrt": "SQRT", "sin": "SIN", "cos": "COS", "tan": "TAN",
            "log": "LOG"
        }

    def cargar_variables(self, variables_dict):
        """Carga variables desde un diccionario."""
        self.variables = variables_dict

    def generar(self, expresion):
        """Convierte una expresión matemática a código P."""
        self.codigo_p = []  # Limpiar código previo

        # Reemplazar operadores estándar con los equivalentes en código P
        for operador, reemplazo in self.operadores.items():
            expresion = expresion.replace(operador, f" {reemplazo} ")

        # Reemplazar funciones matemáticas estándar con sus equivalentes en código P
        for funcion, reemplazo in self.funciones.items():
            expresion = expresion.replace(funcion + "(", reemplazo + " (")

        tokens = expresion.replace("(", " ( ").replace(")", " ) ").split()
        self.pila_operadores = []  # Pila de operadores
        self.pila_operandos = []   # Pila de operandos (valores)
        self.procesar_expresion(tokens)
        return "\n".join(self.codigo_p)  # Devolver código P generado

    def procesar_expresion(self, tokens):
        precedencia = {
            'ADD': 1, 'SUB': 1, 'MUL': 2, 'DIV': 2, 'MOD': 2,
            'POW': 3, 'SQRT': 4, 'SIN': 4, 'COS': 4, 'TAN': 4,
            'LOG': 4
        }  # Prioridad de operadores

        for token in tokens:
            if token.isdigit():  # Número entero
                self.codigo_p.append(f"PUSH {token}")
                self.pila_operandos.append(token)
            elif token.replace(".", "", 1).isdigit():  # Número decimal
                self.codigo_p.append(f"PUSH {token}")
                self.pila_operandos.append(token)
            elif token in self.variables:  # Variable declarada
                valor = self.variables[token]
                self.codigo_p.append(f"PUSH {valor}")
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
        if operador in {"SQRT", "SIN", "COS", "TAN", "LOG"}:
            if len(self.pila_operandos) < 1:
                return
            a = self.pila_operandos.pop()
            self.codigo_p.append(operador)
            self.pila_operandos.append(f"{operador}({a})")
            return

        # Operadores binarios
        if len(self.pila_operandos) < 2:
            return
        b = self.pila_operandos.pop()
        a = self.pila_operandos.pop()
        self.codigo_p.append(operador)
        self.pila_operandos.append(f"({a} {operador} {b})")


# 📌 Definir variables y expresiones directamente en el código
variables = {
    "x": 10,
    "y": 5,
    "z": 2
}

expresiones = [
    "x + y * z",
    "sqrt(x) + sin(y)",
    "(x + y) / z"
]

# 📌 Generar código P para las expresiones
generador = GeneradorCodigoP()
generador.cargar_variables(variables)

print("\n📌 Generar código P (Máquina de Pila):")
for expresion in expresiones:
    print(f"\nExpresión: {expresion}")
    print(generador.generar(expresion))