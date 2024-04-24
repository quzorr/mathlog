import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QToolBar, QGraphicsView, QGraphicsScene,
                             QGraphicsItemGroup, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsItem,
                             QGraphicsLineItem)
from PyQt5.QtGui import QFont, QPen, QPainter, QColor
from PyQt5.QtCore import Qt, QRectF, QLineF


class StateItem(QGraphicsItemGroup):
    def __init__(self, name, is_final=False):
        super().__init__()

        # Основной круг
        self.main_circle = QGraphicsEllipseItem(0, 0, 50, 50)
        self.main_circle.setBrush(Qt.white)
        self.addToGroup(self.main_circle)

        # Внутренний круг для финальных состояний
        self.inner_circle = QGraphicsEllipseItem(5, 5, 40, 40)
        self.inner_circle.setPen(QPen(Qt.black, 1.5, Qt.DotLine))
        self.addToGroup(self.inner_circle)
        self.inner_circle.hide()

        # Текстовая метка
        self.label = QGraphicsTextItem(name, self)
        self.label.setFont(QFont("Arial", 10))
        self.label.setPos(15, 15)
        self.addToGroup(self.label)

        # Установка флагов для перемещения и выделения
        self.setFlags(
            QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)

        # Установка состояния
        self.set_final(is_final)

    def set_final(self, is_final):
        self.inner_circle.setVisible(is_final)

    def toggle_final(self):
        self.set_final(not self.inner_circle.isVisible())

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Переключаем финальное состояние по двойному клику
            self.toggle_final()
        super().mouseDoubleClickEvent(event)


class FSMEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.state_id = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Finite State Machine Editor')
        self.setGeometry(100, 100, 800, 600)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        importAction = QAction('Import', self)
        exportAction = QAction('Export', self)
        fileMenu.addAction(importAction)
        fileMenu.addAction(exportAction)

        self.toolbar = QToolBar("Toolbar")
        self.addToolBar(self.toolbar)
        addAction = QAction('Add State', self)
        self.toolbar.addAction(addAction)

        addAction.triggered.connect(self.addState)

    def addState(self):
        name = "q" + str(self.state_id)
        state = StateItem(name)
        self.scene.addItem(state)
        state.setPos(self.view.mapToScene(self.view.viewport().rect().center()))
        self.state_id += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FSMEditor()
    ex.show()
    sys.exit(app.exec_())
