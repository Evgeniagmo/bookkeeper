from inspect import get_annotations
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category


class ExpensePresenter:

    def __init__(self, model, view, cat_repo, exp_repo):
        self.model = model
        self.view = view
        self.cat_repo = cat_repo
        self.cat_data = []
        for single_cat in self.cat_repo.get_all():
            self.cat_data.append(
                single_cat.make_tuple_from_attr(get_annotations(Category)))

        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.view.on_expense_delete_button_clicked(self.handle_expense_delete_button_clicked)
        self.exp_repo = exp_repo
        self.exp_data = []
        for single_exp in self.exp_repo.get_all():
            self.exp_data.append(
                single_exp.make_tuple_from_attr(get_annotations(Expense)))

    def update_expense_data(self):
        data = []
        for single_exp in self.exp_repo.get_all():
            row_exp = list(single_exp.make_tuple_from_attr(get_annotations(Expense)))
            for cat_tup in self.cat_data:
                if cat_tup[-1] == row_exp[1]:
                    row_exp[1] = cat_tup[0]
                    break
            data.append(row_exp)
        self.view.set_expense_table(data)

    def show(self):
        self.view.show()
        self.update_expense_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self):
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        exp = Expense(amount, cat_pk)
        self.exp_repo.add(exp)
        self.update_expense_data()
        # print(cat_pk, amount)

    def handle_expense_delete_button_clicked(self):
        exp_pk = self.view.get_selected_exp()
        self.exp_repo.delete(exp_pk)
        self.update_expense_data()
        # print(exp_pk)
