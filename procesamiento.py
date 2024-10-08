import json


def cargar_json(rutaArchivo):
    """Carga el archivo JSON desde la ruta especificada."""
    with open(rutaArchivo, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos


def encontrarBloquesPorTipo(datos, tipoPieza):
    """Encuentra bloques que contienen una pieza de un tipo específico."""
    bloquesConPieza = set()  # Usar un conjunto para evitar duplicados

    # Buscar en los bloques predeterminados
    for bloque in datos["def"]["DefaultBlocks"]:
        for pieza in bloque.get("Pieces", []):
            if pieza.get("type") == tipoPieza:
                bloquesConPieza.add(bloque["Name"])

    # Buscar en la lista de bloques
    for bloque in datos["def"]["BlockList"]:
        for pieza in bloque.get("Pieces", []):
            if pieza.get("type") == tipoPieza:
                bloquesConPieza.add(bloque["Name"])

    return list(bloquesConPieza)  # Convertir de nuevo a lista


def encontrarBloquesPorVariable(datos, variableBuscada):
    """Encuentra bloques que contienen una variable específica."""
    bloquesConVariable = set()  # Usar un conjunto para evitar duplicados

    # Buscar en los bloques predeterminados
    for bloque in datos["def"]["DefaultBlocks"]:
        for pieza in bloque.get("Pieces", []):
            if pieza.get("VariableName") == variableBuscada:
                bloquesConVariable.add(bloque["Name"])

    # Buscar en la lista de bloques
    for bloque in datos["def"]["BlockList"]:
        for pieza in bloque.get("Pieces", []):
            if pieza.get("VariableName") == variableBuscada:
                bloquesConVariable.add(bloque["Name"])

    return list(bloquesConVariable)  # Convertir de nuevo a lista
