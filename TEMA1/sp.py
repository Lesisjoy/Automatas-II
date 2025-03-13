class VerificadorTipos:
    TIPO_INT = "int"
    TIPO_FLOAT = "float"
    TIPO_STRING = "string"
    TIPO_CHAR = "char"
    TIPO_BOOL = "bool"

    def __init__(self):
        self.tipos_variables = {}  # Diccionario para almacenar variables y sus tipos
        self.tabla_simbolos = {}  # Diccionario para la tabla de símbolos

    def declarar_variable(self, nombre, tipo):
        """Declara una nueva variable sin asignarle un valor."""
        if nombre in self.tipos_variables:
            print(f"⚠ Advertencia: La variable '{nombre}' ya estaba declarada.")
        else:
            self.tipos_variables[nombre] = tipo
            self.tabla_simbolos[nombre] = {
                "tipo": tipo,
                "direccion": hex(id(nombre)),  # Simulación de dirección de memoria
                "valor": None
            }
            # print(f"✅ Variable declarada: {nombre} ({tipo})")

    def determinar_tipo(self, valor):
        """Determina el tipo de un valor dado."""
        valor = valor.strip()

        if valor.lower() in ['true', 'false']:
            return self.TIPO_BOOL
        if len(valor) == 3 and valor.startswith("'") and valor.endswith("'"):  # Detectar char ('a')
            return self.TIPO_CHAR
        if len(valor) > 1 and valor.startswith('"') and valor.endswith('"'):  # Detectar string ("Hola")
            return self.TIPO_STRING
        try:
            int(valor)
            return self.TIPO_INT
        except ValueError:
            try:
                float(valor)
                return self.TIPO_FLOAT
            except ValueError:
                return self.TIPO_STRING  # Si no es otro tipo, se asume string

    def verificar_asignacion(self, variable, valor):
        """Verifica si la asignación de valor es compatible con la variable."""
        if variable not in self.tipos_variables:
            print(f"❌ Error: La variable '{variable}' no ha sido declarada.")
            return

        tipo_variable = self.tipos_variables[variable]
        tipo_valor = self.determinar_tipo(valor)

        if tipo_variable == tipo_valor:
            self.tabla_simbolos[variable]["valor"] = valor
            print(f"✅ Asignación válida: {variable} ({tipo_variable}) = {valor} ({tipo_valor})")
        elif tipo_variable == self.TIPO_FLOAT and tipo_valor == self.TIPO_INT:
            self.tabla_simbolos[variable]["valor"] = float(valor)  # Conversión implícita permitida
            print(f"✅ Coerción permitida: {variable} ({tipo_variable}) = {valor} ({tipo_valor})")
        elif tipo_variable == self.TIPO_INT and tipo_valor == self.TIPO_FLOAT:
            print(f"⚠ Advertencia: Conversión de float a int en '{variable}', posible pérdida de datos.")
            self.tabla_simbolos[variable]["valor"] = int(float(valor))  # Conversión
        elif tipo_variable == self.TIPO_CHAR and tipo_valor == self.TIPO_STRING:
            print(f"❌ Error: No se puede asignar un string a un char en '{variable}'.")
        else:
            print(f"❌ Error: No se puede asignar {tipo_valor} a {tipo_variable} en '{variable}'.")

    def mostrar_tabla_simbolos(self):
        """Muestra la tabla de símbolos con variables, tipos y valores."""
        print("\n📌 Tabla de Símbolos:")
        print(f"{'Símbolo':<10}{'Tipo':<10}{'Dirección':<15}{'Valor Inicial'}")
        print("-" * 45)
        for var, datos in self.tabla_simbolos.items():
            valor = datos["valor"] if datos["valor"] is not None else "No asignado"
            print(f"{var:<10}{datos['tipo']:<10}{datos['direccion']:<15}{valor}")

# 📌 Leer datos de 'datos2.txt' y procesarlos
verificador = VerificadorTipos()

try:
    with open("datos2.txt", "r", encoding="utf-8") as archivo:
        print("\n📌 Verificador de Tipos:")
        for linea in archivo:
            linea = linea.strip()
            
            # Ignorar líneas vacías y comentarios
            if not linea or linea.startswith("#"):
                continue  

            if linea.startswith("DECLARAR"):  # Declaración de variables
                partes = linea.split()
                if len(partes) == 3:
                    _, nombre, tipo = partes
                    if tipo in [verificador.TIPO_INT, verificador.TIPO_FLOAT, verificador.TIPO_STRING,
                                verificador.TIPO_CHAR, verificador.TIPO_BOOL]:
                        verificador.declarar_variable(nombre, tipo)
                    else:
                        print(f"❌ Error: Tipo '{tipo}' no reconocido en la declaración de '{nombre}'.")
                else:
                    print(f"❌ Error de sintaxis en declaración: {linea}")
            elif "=" in linea:  # Asignaciones
                nombre_variable, valor = map(str.strip, linea.split("=", 1))

                # Eliminar comentarios al final de la línea
                if "#" in valor:
                    valor = valor.split("#")[0].strip()

                verificador.verificar_asignacion(nombre_variable, valor)
            else:
                print(f"⚠ Advertencia: Línea no reconocida '{linea}'.")

    verificador.mostrar_tabla_simbolos()

except FileNotFoundError:
    print("❌ Error: No se encontró el archivo 'datos2.txt'.")

