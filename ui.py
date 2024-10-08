import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QComboBox,
    QTextEdit,
    QHBoxLayout,
)

from PyQt6.QtGui import QIcon

from procesamiento import (
    cargar_json,
    encontrarBloquesPorTipo,
    encontrarBloquesPorVariable,
)


class SelectorArchivos(QWidget):
    def __init__(self):
        super().__init__()

        # ícono de la ventana
        self.setWindowIcon(QIcon("yflow.ico"))

        # Inicializar variables
        self.datos = None
        self.piezaMap = {}  # Mapa para convertir nombres amigables a nombres técnicos

        # Layout principal
        self.layoutPrincipal = QVBoxLayout()

        # Layout para el input de ruta y el botón de examinar
        self.layoutRuta = QHBoxLayout()

        # Botón pequeño para examinar archivos
        self.botonExaminar = QPushButton("Examinar", self)
        self.botonExaminar.clicked.connect(self.examinarArchivo)
        self.layoutRuta.addWidget(self.botonExaminar)

        # Campo de entrada para la ruta
        self.entradaRuta = QLineEdit(self)
        self.layoutRuta.addWidget(self.entradaRuta)

        # Añadir el layout horizontal al layout principal
        self.layoutPrincipal.addLayout(self.layoutRuta)

        # Botón para seleccionar una pieza
        self.botonSeleccionarPieza = QPushButton("Buscar", self)
        self.botonSeleccionarPieza.clicked.connect(self.seleccionarPieza)
        self.layoutPrincipal.addWidget(self.botonSeleccionarPieza)

        # Dropdown de piezas (lista desplegable)
        self.desplegablePiezas = QComboBox(self)
        self.desplegablePiezas.setVisible(
            False
        )  # Oculto hasta que se presione el botón
        self.layoutPrincipal.addWidget(self.desplegablePiezas)

        # Área de texto para mostrar los resultados
        self.areaResultados = QTextEdit(self)
        self.areaResultados.setReadOnly(True)
        self.layoutPrincipal.addWidget(self.areaResultados)

        # Campo de entrada para la variable
        self.entradaVariable = QLineEdit(self)
        self.entradaVariable.setPlaceholderText("Ingresa el nombre de la variable")
        self.layoutPrincipal.addWidget(self.entradaVariable)

        # Botón para buscar por variable
        self.botonBuscarVariable = QPushButton("Buscar variable", self)
        self.botonBuscarVariable.clicked.connect(self.buscarVariable)
        self.layoutPrincipal.addWidget(self.botonBuscarVariable)

        # Configurar el layout principal
        self.setLayout(self.layoutPrincipal)

    def examinarArchivo(self):
        # Función para abrir el diálogo de selección de archivos
        rutaArchivo, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar un flujo", "", "JSON Files (*.json)"
        )
        if rutaArchivo:
            self.entradaRuta.setText(rutaArchivo)
            # Cargar el archivo JSON
            try:
                self.datos = cargar_json(rutaArchivo)
                self.areaResultados.setText("Archivo cargado correctamente.")
                self.cargarTiposPiezas()  # Cargar las piezas en el desplegable
                self.desplegablePiezas.setVisible(
                    True
                )  # Mostrar desplegable cuando el archivo se carga
            except Exception as e:
                self.areaResultados.setText(f"Error al cargar el archivo: {str(e)}")

    def cargarTiposPiezas(self):
        # Crear un set para evitar duplicados
        tiposPiezas = set()

        # Buscar tipos de piezas en los bloques predeterminados
        for bloque in self.datos["def"]["DefaultBlocks"]:
            for pieza in bloque.get("Pieces", []):
                tipo = pieza.get("__type")
                if tipo:
                    tiposPiezas.add(tipo)

        # Diccionario para mapear nombres técnicos a nombres bonitos
        nombresBonitos = {
            "variable-condition-piece": "Condición sobre una variable",
            "shorten-url": "Acortar Url",
            "update-profile-piece": "Actualizar perfil",
            "evaluate-commands-piece": "Evaluar comandos",
        }

        # Limpiar el mapa y el desplegable antes de llenarlos
        self.piezaMap.clear()
        self.desplegablePiezas.clear()

        # Añadir nombres amigables al desplegable y mapearlos a los nombres técnicos
        for tipo in tiposPiezas:
            nombreBonito = nombresBonitos.get(
                tipo, tipo
            )  # Usa el nombre técnico si no hay un bonito
            self.piezaMap[nombreBonito] = tipo  # Mapear nombre bonito a nombre técnico
            self.desplegablePiezas.addItem(nombreBonito)

    def seleccionarPieza(self):
        # Función para buscar bloques por tipo de pieza
        nombreBonito = (
            self.desplegablePiezas.currentText()
        )  # Obtener el nombre bonito seleccionado
        tipoPieza = self.piezaMap.get(
            nombreBonito
        )  # Obtener el nombre técnico correspondiente
        if self.datos and tipoPieza:
            bloques = encontrarBloquesPorTipo(self.datos, tipoPieza)
            if bloques:
                textoResultado = f"Los bloques que contienen piezas del tipo '{nombreBonito}' son:\n\n"
                textoResultado += "\n".join(f"{bloque}" for bloque in bloques)
            else:
                textoResultado = (
                    f"No se encontraron bloques con piezas del tipo '{nombreBonito}'."
                )
            self.areaResultados.setText(textoResultado)
        else:
            self.areaResultados.setText("Primero debes cargar un archivo JSON.")

    def buscarVariable(self):
        # Obtener el nombre de la variable del campo de texto
        variableBuscada = self.entradaVariable.text()
        if self.datos and variableBuscada:
            bloques = encontrarBloquesPorVariable(self.datos, variableBuscada)
            if bloques:
                textoResultado = f"Los bloques que contienen la variable '{variableBuscada}' son:\n\n"
                textoResultado += "\n".join(f"{bloque}" for bloque in bloques)
            else:
                textoResultado = (
                    f"No se encontraron bloques con la variable '{variableBuscada}'."
                )
            self.areaResultados.setText(textoResultado)
        else:
            self.areaResultados.setText(
                "Primero debes cargar un archivo JSON y especificar una variable."
            )


# Código principal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    selector = SelectorArchivos()
    selector.setWindowTitle("Buscador yFlow")
    selector.show()
    sys.exit(app.exec())
