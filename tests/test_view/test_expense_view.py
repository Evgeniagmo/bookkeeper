from bookkeeper.view.expense_view import MainWindow, TableModel
import pytest


def test_columnCount(qtbot):
    exp_list = [['smth', 1], ['smth', 2]]
    widget = TableModel(exp_list)
    assert widget._data == exp_list

def test_rowCount(qtbot):
    exp_list = [['smth', 1], ['smth', 2]]
    widget = TableModel(exp_list)
    index = 1
    assert widget.rowCount(index) == 2

def test_columnCount(qtbot):
    exp_list = [['smth', 1], ['smth', 2]]
    widget = TableModel(exp_list)
    index = 1
    assert widget.columnCount(index) == 2


def test_set_expense_table(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)
    exp_list = ('123', '456')
    with pytest.raises(ValueError):
        widget.set_expense_table(exp_list)

def test_set_category_dropdown(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)
    cat_list = [('smth', 1), ('smth', 2)]
    widget.set_category_dropdown(cat_list)
    qtbot.keyClicks(widget.category_dropdown, '2 smth')
    assert widget.category_dropdown.currentIndex() == 1
def test_get_amount_int(qtbot):

    widget = MainWindow()
    qtbot.addWidget(widget)
    qtbot.keyClicks(widget.amount_line_edit, '123')
    assert widget.amount_line_edit.text() == '123'
    assert widget.get_amount() == 123

def test_get_amount_float(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)
    qtbot.keyClicks(widget.amount_line_edit, '123,45')
    assert widget.get_amount() == 123.45
def test_get_selected_cat(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)
    widget.category_dropdown.addItems(['1 smth', '2 smth'])
    qtbot.keyClicks(widget.category_dropdown, '2 smth')
    assert widget.get_selected_cat() == 2
def test_get_selected_exp(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)
    qtbot.keyClicks(widget.exp_pk_line_edit, '123')
    assert widget.get_selected_exp() == 123




