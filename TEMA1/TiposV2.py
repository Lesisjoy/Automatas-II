class VerificadorTipos:
    TIPO_INT = "int"
    TIPO_FLOAT = "float"
    TIPO_STRING = "string"
    TIPO_BOOL = "bool"

    def __init__(self):
        self.tipos_variables = {}  # Almacena las variables y sus tipos

    def declarar_variable(self, nombre, tipo):
        """ Registra una nueva variable con su tipo """
        self.tipos_variables[nombre] = tipo

    def determinar_tipo(self, valor):
        """ Determina el tipo de un valor dado """
        valor = str(valor).strip()  # Convertir a cadena y eliminar espacios
        if valor.lower() in ['true', 'false']:
            return self.TIPO_BOOL
        try:
            int(valor)
            return self.TIPO_INT
        except ValueError:
            try:
                float(valor)
                return self.TIPO_FLOAT
            except ValueError:
                return self.TIPO_STRING

    def obtener_tipo_variable(self, variable):
        """ Obtiene el tipo de una variable declarada """
        return self.tipos_variables.get(variable, None)

    def verificar_asignacion(self, variable, valor):
        """ Verifica si la asignación de valor es compatible con la variable """
        tipo_variable = self.obtener_tipo_variable(variable)
        tipo_valor = self.determinar_tipo(valor)

        if tipo_variable is None:
            raise ValueError(f"Error: La variable '{variable}' no está declarada.")

        # Reglas de compatibilidad de tipos
        if tipo_variable == tipo_valor:
            print(f"Asignación válida: {variable} ({tipo_variable}) = {valor} ({tipo_valor})")
        elif tipo_variable == self.TIPO_FLOAT and tipo_valor == self.TIPO_INT:
            print(f"Coerción permitida: {variable} ({tipo_variable}) = {valor} ({tipo_valor})")
        elif tipo_variable == self.TIPO_INT and tipo_valor == self.TIPO_FLOAT:
            print(f"⚠ Advertencia: Conversión de float a int en '{variable}', posible pérdida de datos.")
        else:
            raise TypeError(f"Error: No se puede asignar {tipo_valor} a {tipo_variable} en '{variable}'.")


# Prueba del verificador de tipos
verificador = VerificadorTipos()

# Declaración de variables
verificador.declarar_variable("x", VerificadorTipos.TIPO_INT)
verificador.declarar_variable("y", VerificadorTipos.TIPO_FLOAT)
verificador.declarar_variable("nombre", VerificadorTipos.TIPO_STRING)
verificador.declarar_variable("es_valido", VerificadorTipos.TIPO_BOOL)

# Asignaciones de prueba
verificador.verificar_asignacion("x", "5")       # ✅ Válido (int = int)
verificador.verificar_asignacion("y", "5")       # ✅ Válido (coerción int → float)
verificador.verificar_asignacion("x", "3.5")     # ⚠ Advertencia: float a int
verificador.verificar_asignacion("nombre", "a") # ❌ Error: int no puede asignarse a string
verificador.verificar_asignacion("es_valido", "true") # ✅ Válido (bool = bool)
