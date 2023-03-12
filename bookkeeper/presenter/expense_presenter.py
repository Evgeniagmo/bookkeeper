from inspect import get_annotations
from bookkeeper.models.expense import Expense


class ExpensePresenter:

    def __init__(self, model, view, cat_repo, exp_repo):
        self.model = model
        self.view = view
        self.cat_data = cat_repo.get_all()
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.exp_repo = exp_repo
        self.exp_data = []
        for single_exp in self.exp_repo.get_all():
            self.exp_data.append(
                single_exp.make_tuple_from_attr(get_annotations(Expense)))

    def show(self):
        self.view.show()
        self.view.set_expense_table(self.exp_data)
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self):

        # TODO: надо обновить таблицу после добавления

        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        exp = Expense(amount, cat_pk)
        self.exp_repo.add(exp)
        print(cat_pk, amount)


