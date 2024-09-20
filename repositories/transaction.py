from entities.transaction import TransactionEntity
from sqlalchemy import func

from entities.user import UserEntity


class TransactionRepository:
    def __init__(self, session):
        self._session = session

    def get_user_with_lock(self, user_id):
        return self._session.query(UserEntity).filter(
            UserEntity.id == user_id
        ).with_for_update(nowait=True).one()

    def update_user_balance(self, entity: UserEntity):
        self._session.add(entity)

    def create_transaction(self, entity: TransactionEntity):
        self._session.add(entity)

    def get_total_transaction_amount(self):
        total_amount = self._session.query(
            func.sum(TransactionEntity.amount)
        ).filter(
            TransactionEntity.state == TransactionEntity.TransactionState.INITIATED
        ).scalar()
        return total_amount if total_amount else 0

    def list_transaction(self, state=None):
        query = self._session.query(TransactionEntity)
        if state:
            query = query.filter(TransactionEntity.state == state)
        return query.all()

    def list_transaction_with_lock(self, state):
        query = self._session.query(TransactionEntity)
        if state:
            query = query.filter(TransactionEntity.state == state)
        return query.with_for_update().all()

    def update_transactions_state(self, ids, new_state):
        self._session.query(TransactionEntity).filter(
            TransactionEntity.id.in_(ids)
        ).update(
            {TransactionEntity.state: new_state},
            synchronize_session='fetch'
        )

    def update_transactions_into_from_pending_to_initiate(self):
        with self:
            self._session.query(
                TransactionEntity,
            ).filter(
                TransactionEntity.state == TransactionEntity.TransactionState.PROCESSING,
            ).update(
                {TransactionEntity.state: TransactionEntity.TransactionState.INITIATED},
                synchronize_session='fetch',
            )