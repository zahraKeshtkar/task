from repositories.transaction import TransactionRepository
from repositories.currency import CurrencyRepository


class UnitOfWork:
    def __init__(self, session):
        self.session = session
        self.transaction_repo = TransactionRepository(self.session)
        self.currency_repo = CurrencyRepository(self.session)
        self._in_transaction = False

    def __enter__(self):
        self._in_transaction = True
        self.session.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    def commit(self):
        if self._in_transaction:
            self.session.commit()
            self._in_transaction = False

    def rollback(self):
        if self._in_transaction:
            self.session.rollback()
            self._in_transaction = False

