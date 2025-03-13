class VerificadorTipos:
    def __init__(self):
        self.tipos_variables = {}  # Almacena las variables y sus tipos

    def declarar_variable(self, nombre, tipo):
        """ Registra una nueva variable con su tipo """
        self.tipos_variables[nombre] = tipo

    def verificar_asignacion(self, variable, valor):
        """ Verifica si la asignación de valor es compatible con la variable """
        tipo_variable = self.tipos_variables.get(variable, None)
        tipo_valor = self.determinar_tipo(valor)

        if tipo_variable is None:
            print(f"Error: La variable '{variable}' no está declarada.")
            return

        # Reglas de compatibilidad de tipos
        if tipo_variable == tipo_valor:
            print(f"Asignación válida: {variable} ({tipo_variable}) = {valor} ({tipo_valor})")
        elif tipo_variable == "float" and tipo_valor == "int":
            print(f"Coerción permitida: {variable} ({tipo_variable}) = {valor} ({tipo_valor})")
        elif tipo_variable == "int" and tipo_valor == "float":
            print(f"⚠ Advertencia: Conversión de float a int en '{variable}', posible pérdida de datos.")
        else:
            print(f"❌ Error: No se puede asignar {tipo_valor} a {tipo_variable} en '{variable}'.")

    def determinar_tipo(self, valor):
        """ Determina el tipo de un valor dado """
        try:
            int(valor)
            return "int"
        except ValueError:
            try:
                float(valor)
                return "float"
            except ValueError:
                return "string"

# Prueba del verificador de tipos
verificador = VerificadorTipos()

# Declaración de variables
verificador.declarar_variable("x", "int")
verificador.declarar_variable("y", "float")
verificador.declarar_variable("nombre", "string")

# Asignaciones de prueba
verificador.verificar_asignacion("x", "5")       # ✅ Válido (int = int)
verificador.verificar_asignacion("y", "5")       # ✅ Válido (coerción int → float)
verificador.verificar_asignacion("x", "3.5")     # ⚠ Advertencia: float a int
verificador.verificar_asignacion("nombre", "45") # ❌ Error: int no puede asignarse a string
verificador.verificar_asignacion("z", "5")       # ❌ Error: Variable no declarada
