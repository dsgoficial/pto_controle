from qgis.PyQt.QtWidgets import (
    QLineEdit
)

from processing.gui.wrappers import WidgetWrapper


class MyWidgetWrapper(WidgetWrapper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = args[0]

    def createWidget(self):
        self._lineedit = QLineEdit()
        # Qt6 exige o enum ESCOPADO. O `QLineEdit.Password` de Qt5 nao existe mais e
        # levanta AttributeError ao abrir a janela de qualquer algoritmo com senha.
        self._lineedit.setEchoMode(QLineEdit.EchoMode.Password)
        # if self.placeholder:
        #     self._lineedit.setPlaceholderText(self.placeholder)
        return self._lineedit

    def value(self):
        return self._lineedit.text()