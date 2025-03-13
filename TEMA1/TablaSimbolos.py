class TablaSimbolos:
    def __init__(self):
        self.tabla = {}  # Diccionario para almacenar los símbolos
        self.direccion_base = 0x1000  # Dirección base de memoria

    def agregar_simbolo(self, nombre, tipo, valor=None):
        """ Agrega un símbolo a la tabla con su tipo, dirección y valor inicial """
        if nombre in self.tabla:
            print(f"Error: La variable '{nombre}' ya está declarada.")
            return
        
        direccion = hex(self.direccion_base + len(self.tabla))  # Generar dirección única
        self.tabla[nombre] = {"tipo": tipo, "direccion": direccion, "valor": valor}

    def obtener_simbolo(self, nombre):
        """ Devuelve la información de un símbolo si existe """
        return self.tabla.get(nombre, f"Error: La variable '{nombre}' no está declarada.")

    def mostrar_tabla(self):
        """ Muestra la tabla de símbolos """
        print("\nTabla de Símbolos:")
        print(f"{'Símbolo':<10} {'Tipo':<10} {'Dirección':<10} {'Valor Inicial'}")
        print("-" * 40)
        for nombre, info in self.tabla.items():
            print(f"{nombre:<10} {info['tipo']:<10} {info['direccion']:<10} {info['valor']}")

# Prueba del sistema de tabla de símbolos
tabla = TablaSimbolos()

# Simulación de declaraciones en un código fuente en C
tabla.agregar_simbolo("a", "int", 5)
tabla.agregar_simbolo("b", "float", 2.5)
tabla.agregar_simbolo("c", "int", None)  # No tiene valor inicial
tabla.agregar_simbolo("d", "char", "'X'")

# Mostrar la tabla de símbolos generada
tabla.mostrar_tabla()

# Consultar información de una variable
print("\nConsulta de la variable 'b':", tabla.obtener_simbolo("b"))
print("Consulta de la variable 'x':", tabla.obtener_simbolo("x"))  # Variable no declarada