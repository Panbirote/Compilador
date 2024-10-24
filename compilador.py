import re
arrayAritmetico = {
    "+",
    "-",
    "*",
    "/",
    "%",
    "^",
}

arrayRelacional = {
    # "=",
    "!=",
    ">",
    "<",
    ">=",
    "<=",
    "==",
}

arrayLogico = {
    "&",
    "||",
    "!",
}

arrayAsignacion = {
    "=",
    "+=",
    "-=",
    "*=",
    "%=",
    "/=",
}

arrayEspecial = {
    ";", 
    ",", 
    "(", 
    ")", 
    "{", 
    "}", 
    "[", 
    "]", 
    ":"
}

class Nodo:
    def __init__(self, tipo, lexema, valor, renglon, columna):
        self.tipo = tipo  # Tipo del token (Identificador, Palabra reservada, Símbolo, etc.)
        self.lexema = lexema  # El texto que representa el token
        self.valor = valor  # El valor del token (en este caso es el mismo que el lexema)
        self.renglon = renglon  # El número de línea en la que apareció el token
        self.columna = columna  # La columna en la que se encontró el token
        self.siguiente = None  # Puntero al siguiente nodo (al ser una lista enlazada)

# Crea un nuevo nodo y lo retorna
def crear_nodo(tipo, lexema, valor, renglon, columna):
    return Nodo(tipo, lexema, valor, renglon, columna)

# Agrega un nodo al final de la lista enlazada
def agregar_nodo(lista, tipo, lexema, valor, renglon, columna):
    nuevo_nodo = crear_nodo(tipo, lexema, valor, renglon, columna)
    if lista is None:
        return nuevo_nodo  # Si la lista está vacía, el nuevo nodo es la cabeza
    else:
        temp = lista
        while temp.siguiente is not None:  # Recorremos hasta el último nodo
            temp = temp.siguiente
        temp.siguiente = nuevo_nodo  # Añadimos el nuevo nodo al final
    return lista

# Imprimir los nodos en formato de tabla
def imprimir_lista(lista):
    temp = lista
    print("+------------+------------------+------------------+----------+----------+")
    print("| Lexema     | Tipo             | Valor            | Renglon  | Columna  |")
    print("+------------+------------------+------------------+----------+----------+")
    while temp is not None:
        if (temp.valor.isdigit()) :
            print(f"| {temp.lexema:<10} | {temp.tipo:<16} | {temp.valor:<16} | {temp.renglon:<8} | {temp.columna:<8} |")
        else :
            print(f"| {temp.lexema:<10} | {temp.tipo:<16} |                  | {temp.renglon:<8} | {temp.columna:<8} |")
            
        temp = temp.siguiente  # Pasamos al siguiente nodo
    print("+------------+------------------+------------------+----------+----------+")

# Verifica si la lista de tokens está vacía
def lista_esta_vacia(lista):
    return lista is None

# Lista de palabras reservadas
palabras_reservadas = [
    "Si", "Sino", "Mientras", "para", "Entero", "Flotante", "Caracter", "Volver", "Regresa", "Ir",
    "vacio", "Romper", "Continuar", "switch", "Caso", "Predeter", "Clase", "Flotante", "Constante"
]

# Función que verifica si un lexema es una palabra reservada
def es_palabra_reservada(lexema):
    return lexema in palabras_reservadas

# Función que verifica si un lexema es un símbolo especial
def es_simbolo_especial(lexema):
    return lexema in arrayEspecial

# Función que verifica si un lexema es un símbolo aritmetico
def es_simbolo_Aritmetico(lexema):
    return lexema in arrayAritmetico

# Función que verifica si un lexema es un símbolo relacional
def es_simbolo_Relacional(lexema):
    return lexema in arrayRelacional

# Función que verifica si un lexema es un símbolo Logifoc
def es_simbolo_Logico(lexema):
    return lexema in arrayLogico

# Función que verifica si un lexema es un símbolo asignacion
def es_simbolo_Asignacion(lexema):
    return lexema in arrayAsignacion

# Función que verifica si un carácter es un símbolo especial
def es_simbolo_especial_caracter(c):
    if es_simbolo_especial(c):
        return True
    elif es_simbolo_Aritmetico(c):
        return True
    elif es_simbolo_Relacional(c):
        return True
    elif es_simbolo_Logico(c):
        return True
    else :
        return False

# Automata que procesa identificadores y palabras reservadas
def automata_identificador(linea, i, renglon, lista_tokens):
    lexema = []
    # Mientras el carácter sea alfanumérico o subrayado, lo añadimos al lexema
    while i < len(linea) and (linea[i].isalnum() or linea[i] == '_'):
        lexema.append(linea[i])
        i += 1
    lexema = ''.join(lexema)  # Convertimos la lista de caracteres a una cadena

    # Determinamos si es una palabra reservada o un identificador
    if es_palabra_reservada(lexema):
        lista_tokens = agregar_nodo(lista_tokens, "Palabra reservada", lexema, lexema, renglon, i - len(lexema) + 1)
    else:
        lista_tokens = agregar_nodo(lista_tokens, "Identificador", lexema, lexema, renglon, i - len(lexema) + 1)
    return i - 1, lista_tokens  # Retrocedemos una posición para no saltar el siguiente carácter

# Automata que procesa números enteros y reales
def automata_numero(linea, i, renglon, lista_tokens):
    lexema = []
    es_real = False  # Para marcar si el número tiene parte decimal

    # Mientras sea un dígito o un punto decimal (solo permitimos un punto)
    while i < len(linea) and (linea[i].isdigit() or (linea[i] == '.' and not es_real)):
        if linea[i] == '.':
            es_real = True
        lexema.append(linea[i])
        i += 1
    lexema = ''.join(lexema)

    # Si el número tiene punto decimal, es un número real, si no, es entero
    if es_real:
        lista_tokens = agregar_nodo(lista_tokens, "Numero Real", lexema, lexema, renglon, i - len(lexema) + 1)
    else:
        lista_tokens = agregar_nodo(lista_tokens, "Numero Entero", lexema, lexema, renglon, i - len(lexema) + 1)
    return i - 1, lista_tokens

# Automata que maneja símbolos especiales
def automata_simbolo(linea, i, renglon, lista_tokens):
    # Probamos si es un símbolo doble (por ejemplo, "==" o ">=")
    lexemaDoble = linea[i:i+2]
    lexema = linea[i]
    if es_simbolo_Relacional(lexemaDoble):
        lista_tokens = agregar_nodo(lista_tokens, "Simbolo Relacional", lexemaDoble, lexemaDoble, renglon, i + 1)
        i += 1  # Avanzamos dos posiciones porque es un símbolo doble
    elif es_simbolo_Logico(lexemaDoble):
        lista_tokens = agregar_nodo(lista_tokens, "Simbolo Logico", lexemaDoble, lexemaDoble, renglon, i + 1)
        i += 1  # Avanzamos dos posiciones porque es un símbolo doble
    elif es_simbolo_Asignacion(lexemaDoble):
        lista_tokens = agregar_nodo(lista_tokens, "Simbolo Asignación", lexemaDoble, lexemaDoble, renglon, i + 1)
        i += 1  # Avanzamos dos posiciones porque es un símbolo doble
    elif es_simbolo_Aritmetico(lexema):
        lista_tokens = agregar_nodo(lista_tokens, "Simbolo Aritmetico", lexema, lexema, renglon, i + 1)
    elif es_simbolo_Asignacion(lexema):
        lista_tokens = agregar_nodo(lista_tokens, "Simbolo Asignación", lexema, lexema, renglon, i + 1)
    elif es_simbolo_Relacional(lexema):
        lista_tokens = agregar_nodo(lista_tokens, "Simbolo Relacional", lexema, lexema, renglon, i + 1)
    elif es_simbolo_Logico(lexema):
        lista_tokens = agregar_nodo(lista_tokens, "Simbolo Logico", lexema, lexema, renglon, i + 1)
    elif es_simbolo_especial(lexema):
        lista_tokens = agregar_nodo(lista_tokens, "Simbolo Especial", lexema, lexema, renglon, i + 1)
    return i, lista_tokens

    
# Función que analiza una línea completa de texto
def analizar(linea, renglon, lista_tokens):
    i = 0
    while i < len(linea):
        if linea[i].isalpha() or linea[i] == '_':  # Si es letra o subrayado, es un identificador
            i, lista_tokens = automata_identificador(linea, i, renglon, lista_tokens)
        elif linea[i].isdigit():  # Si es un número, es un token de tipo número
            i, lista_tokens = automata_numero(linea, i, renglon, lista_tokens)
        elif es_simbolo_especial_caracter(linea[i]):  # Si es un símbolo especial
            i, lista_tokens = automata_simbolo(linea, i, renglon, lista_tokens)
        i += 1
    return lista_tokens

# Función principal
def main():
    try:
        with open("D:\compilador\codigo.txt", "r") as archivo:
            lista_tokens = None  # Inicializamos la lista de tokens como vacía
            renglon = 1
            for linea in archivo:
                lista_tokens = analizar(linea.strip(), renglon, lista_tokens)  # Analizamos cada línea
                renglon += 1

            if lista_esta_vacia(lista_tokens):  # Si no hay tokens, lo indicamos
                print("No se encontraron tokens.")
            else:
                imprimir_lista(lista_tokens)  # Imprimimos los tokens en formato de tabla
    except FileNotFoundError:
        print("Error al abrir el archivo.")

if __name__ == "__main__":
    main()
