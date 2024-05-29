import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QToolBar, QGraphicsView, QGraphicsScene,
                             QGraphicsItemGroup, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsItem,
                             QGraphicsLineItem, QInputDialog)
from PyQt5.QtGui import QFont, QPen, QPainter, QColor, QPolygonF
from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF


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

    # def itemChange(self, change, value):
    #     if change == QGraphicsItem.ItemPositionChange:
    #         for arrow in self.scene().items():
    #             if isinstance(arrow, TransitionArrow) and (arrow.start_item is self or arrow.end_item is self):
    #                 arrow.update_position()
    #     return super().itemChange(change, value)

    def mousePressEvent(self, event):
        # Реализация выбора с поддержкой множественного выбора
        if event.modifiers() & Qt.ControlModifier:
            self.setSelected(not self.isSelected())
        else:
            super(StateItem, self).mousePressEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.updateConnectedTransitions()
        return super().itemChange(change, value)

    def updateConnectedTransitions(self):
        # Обновляем положение всех связанных переходов
        for item in self.scene().items():
            if isinstance(item, TransitionArrow) and (item.start_item == self or item.end_item == self):
                item.update_position()


class TransitionArrow(QGraphicsLineItem):
    def __init__(self, start_item, end_item, symbol):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.symbol = symbol
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(-1)  # Устанавливаем стрелки под состояниями

        # Добавление текста для символа перехода
        self.text = QGraphicsTextItem(symbol, self)
        self.text.setFont(QFont("Arial", 10))
        self.update_position()

    def update_position(self):
        line = QLineF(self.start_item.scenePos(), self.end_item.scenePos())
        self.setLine(line)

        # Позиционирование текста перехода в середине стрелки
        self.text.setPos(
            line.pointAt(0.5) - QPointF(self.text.boundingRect().width() / 2, self.text.boundingRect().height()))

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        # Рисуем стрелку в конце линии
        end_point = self.line().p2()
        arrow_head = QPolygonF([end_point + QPointF(-10, 10), end_point + QPointF(-10, -10), end_point])
        painter.drawPolygon(arrow_head)


class FSMEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.state_id = 0
        self.selected_states = []
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

        addTransitionAction = QAction('Add Transition', self)
        self.toolbar.addAction(addTransitionAction)
        addTransitionAction.triggered.connect(self.addTransition)

        self.scene.selectionChanged.connect(self.updateSelectedStates)

    def addState(self):
        name = "q" + str(self.state_id)
        state = StateItem(name)
        self.scene.addItem(state)
        state.setPos(self.view.mapToScene(self.view.viewport().rect().center()))
        self.state_id += 1

    def updateSelectedStates(self):
        current_selection = self.scene.selectedItems()
        if len(current_selection) == 2 and all(isinstance(item, StateItem) for item in current_selection):
            self.selected_states = current_selection
        elif len(current_selection) > 2:
            # Очищаем выбор, если выбрано больше двух элементов
            for item in current_selection:
                if item not in self.selected_states:
                    item.setSelected(False)

    def addTransition(self):
        if len(self.selected_states) == 2:
            symbol, ok = QInputDialog.getText(self, 'Transition Symbol', 'Enter symbol for the transition:')
            if ok and symbol:
                transition = TransitionArrow(self.selected_states[0], self.selected_states[1], symbol)
                self.scene.addItem(transition)
                self.selected_states[0].setSelected(False)
                self.selected_states[1].setSelected(False)
                self.selected_states = []

    def itemMoved(self):
        for item in self.scene.items():
            if isinstance(item, TransitionArrow):
                item.update_position()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FSMEditor()
    ex.show()
    sys.exit(app.exec_())
