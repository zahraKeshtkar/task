from entities.currency import CurrencyEntity

class CurrencyRepository:
    def __init__(self, session):
        self._session = session

    def get_currency_with_id(self, currency_id):
        return self._session.query(CurrencyEntity).filter(
            CurrencyEntity.id == currency_id
        ).one_or_none()

    def list_currencies(self):
        return self._session.query(CurrencyEntity).all()