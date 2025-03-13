class AnalizadorSemantico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    def obtener_token(self):
        if self.posicion < len(self.tokens):
            return self.tokens[self.posicion]
        return None

    def consumir_token(self):
        self.posicion += 1

    def F(self):
        """ F → (E) | número """
        token = self.obtener_token()
        if token.isdigit():
            self.consumir_token()
            return int(token)  # Acción semántica: devolver valor numérico
        elif token == '(':
            self.consumir_token()
            valor = self.E()
            if self.obtener_token() == ')':
                self.consumir_token()
                return valor  # Acción semántica: devolver valor dentro de paréntesis
        raise SyntaxError("Error de sintaxis en F")

    def T(self):
        """ T → T * F | F """
        valor = self.F()
        while self.obtener_token() in ('*', '/'):
            operador = self.obtener_token()
            self.consumir_token()
            if operador == '*':
                valor *= self.F()  # Acción semántica: multiplicar valores
            elif operador == '/':
                valor /= self.F()  # Acción semántica: dividir valores
        return valor

    def E(self):
        """ E → E + T | T """
        valor = self.T()
        while self.obtener_token() in ('+', '-'):
            operador = self.obtener_token()
            self.consumir_token()
            if operador == '+':
                valor += self.T()  # Acción semántica: sumar valores
            elif operador == '-':
                valor -= self.T()  # Acción semántica: restar valores
        return valor

    def analizar(self):
        resultado = self.E()
        if self.posicion < len(self.tokens):
            raise SyntaxError("Error de sintaxis: tokens restantes")
        return resultado

# Prueba del analizador con una expresión
expresion = "3 + 5 * (2 - 4)"
tokens = expresion.replace("(", " ( ").replace(")", " ) ").split()
analizador = AnalizadorSemantico(tokens)
resultado = analizador.analizar()
print(f"Resultado de la expresión '{expresion}': {resultado}")