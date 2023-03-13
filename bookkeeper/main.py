"""
Модуль, откуда запускается приложение
"""

import sys
from PySide6 import QtWidgets
from bookkeeper.view.expense_view import MainWindow
from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository

DB_NAME = r'D:\Py_project1\bookkeeper\test.db'

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    view = MainWindow()
    MODEL = None  # TODO: здесь должна быть модель

    cat_repo = SQLiteRepository[Category](DB_NAME, Category)
    exp_repo = SQLiteRepository[Expense](DB_NAME, Expense)

    # TODO: передать три репозитория
    window = ExpensePresenter(MODEL, view, cat_repo, exp_repo)
    window.show()
    app.exec()
