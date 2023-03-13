"""
Модуль, в котором задаются параметры окон и виджетов в приложении
"""

from typing import Any
from PySide6 import QtCore, QtWidgets, QtGui


class TableModel(QtCore.QAbstractTableModel):
    """
    Модель таблицы расходов, которая отстраивается в соответствии
    с данными в БД Expenses.
    Готовая таблица отображается в основном окне приложения
    """

    def __init__(self, data) -> None:
        super().__init__()
        self._data = data

    def data(self, index: Any, role: int) -> Optional[Any]:
        """
        Структурирует данные в виде таблицы.
        Ряды - внешний список
        Колонки - внутренний список
        """
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index: Any) -> int:
        """
        Определяет количество строк таблицы в окне

        Yields
        -------
        Количество элементов в списке кортежей с данными
        """
        return len(self._data)

    def columnCount(self, index: Any) -> int:
        """
        Определяет количество столбцов для таблицы в окне

        Yields
        -------
        Количество элементов в кортеже с данными
        """
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class MainWindow(QtWidgets.QMainWindow):
    """
    Создать основное окно приложения.
    Задать окна для: таблицы расходов,
                     кнопок добавления расхода в нужной категории
                     кнопок удаления расхода по идентификатору
                     отображения бюджета (ПУСТОЕ)
    """

    def __init__(self) -> None:
        super().__init__()

        self.item_model = None
        self.setWindowTitle("Программа для ведения бюджета")
        self.setFixedSize(500, 600)

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(QtWidgets.QLabel('Последние расходы'))

        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        self.layout.addWidget(QtWidgets.QLabel('Бюджет'))
        self.layout.addWidget(QtWidgets.QLabel(
            '<TODO: таблица бюджета>\n\n\n\n\n\n\n\n'))

        self.bottom_controls = QtWidgets.QGridLayout()

        self.bottom_controls.addWidget(QtWidgets.QLabel('Сумма'), 0, 0)

        self.amount_line_edit = QtWidgets.QLineEdit()
        self.amount_line_edit.setValidator(
            QtGui.QDoubleValidator(1., 100000000., 2, self))
        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)

        self.bottom_controls.addWidget(QtWidgets.QLabel('Категория'), 1, 0)

        self.category_dropdown = QtWidgets.QComboBox()

        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.category_edit_button = QtWidgets.QPushButton('Редактировать')
        self.bottom_controls.addWidget(self.category_edit_button, 1, 2)

        self.expense_add_button = QtWidgets.QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 2, 1)

        self.bottom_controls.addWidget(QtWidgets.QLabel('Номер записи'), 3, 0)

        self.exp_pk_line_edit = QtWidgets.QLineEdit()
        self.exp_pk_line_edit.setValidator(QtGui.QIntValidator(1, 1000000000, self))
        self.bottom_controls.addWidget(self.exp_pk_line_edit, 3, 1)

        self.expense_delete_button = QtWidgets.QPushButton('Удалить')
        self.bottom_controls.addWidget(self.expense_delete_button, 4, 1)

        self.bottom_widget = QtWidgets.QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_expense_table(self, data) -> None:
        """
        Отобразить в виде таблицы текущее содержание БД с расходами

        Parameters
        ----------
        data - список кортежей, содержащих значения атрибутов экземпляров
        класса Expense из БД
        """
        self.item_model = TableModel(data)
        self.expenses_grid.setModel(self.item_model)

    def set_category_dropdown(self, data: list[tuple[Any]]) -> None:
        """
        Отобразить выпадающий список доступных категорий.

        Parameters
        ----------
        data - список кортежей, содержащих значения атрибутов экземпляров
        класса Category из БД
        """
        for tup in data:
            self.category_dropdown.addItems([str(tup[-1]) + ' ' + tup[0]])

    def on_expense_add_button_clicked(self, slot: Any) -> None:
        self.expense_add_button.clicked.connect(slot)

    def on_expense_delete_button_clicked(self, slot: Any) -> None:
        self.expense_delete_button.clicked.connect(slot)

    def get_amount(self) -> float:
        """
        Вернуть сумму нового расхода, введенную пользователем.

        Yields
        -------
        Значение суммы (тип float), которое будет записано в новый объект Expense
        """

        amount = self.amount_line_edit.text()
        if ',' in amount:
            amount = amount.replace(',', '.')
        return float(amount)  # TODO: обработка исключений

    def get_selected_cat(self) -> int:  # TODO: обработка исключений
        """
        Вернуть идентификатор категории, к которой относится новый расход.

        Yields
        -------
        Идентификатор pk, по которому будет добавлен новый объект Expense
        """
        cur_index = self.category_dropdown.currentIndex()
        selected_cat = self.category_dropdown.itemText(cur_index)
        cat_pk = selected_cat.split(maxsplit=1)[0]
        return int(cat_pk)

    def get_selected_exp(self) -> int:
        """
        Вернуть порядковый номер расхода, который требуется удалить.

        Yields
        -------
        Идентификатор pk, по которому будет удален объект Expense
        """
        exp_pk = self.exp_pk_line_edit.text()
        return int(exp_pk)
