"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: float
    category: int
    expense_date: datetime = field(default_factory=datetime.now)
    added_date: datetime = field(default_factory=datetime.now)
    comment: str = ''
    pk: int = 0

    def make_tuple_from_attr(self,
                             attrs: dict[str, Any]) -> tuple[Any]:
        """
        Преобразовать значения атрибутов класса в кортеж. Необходимо
        для более удобного взаимодействия с экземплярами класса в Презентере
        Parameters
        ----------
        attrs - словарь из аннотаций атрибутов класса

        Yields
        -------
        Кортеж, содержащий значения атрибутов данного экземпляра класса
        """
        result = tuple(getattr(self, a) for a in attrs.keys())
        return result
