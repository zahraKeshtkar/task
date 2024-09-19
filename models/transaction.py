from sqlalchemy import Table, Column, Integer, ForeignKey, Enum, Numeric
from sqlalchemy.orm import mapper

from entities.transaction import TransactionEntity
from models.base import uuid_pk_column, meta, temporal_columns, UUIDField

transaction_table = Table(
    'transactions', meta,
    uuid_pk_column(),
    Column(
        'user_id',
        UUIDField,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    ),
    Column(
        'currency_id',
        UUIDField,
        ForeignKey('currencies.id', ondelete='CASCADE'),
        nullable=False
    ),
    Column('count', Integer, nullable=False),
    Column('amount', Numeric(precision=12, scale=2), nullable=False),
    Column('state', Enum(TransactionEntity.TransactionState), nullable=False),
    *temporal_columns()
)

mapper(
    TransactionEntity,
    transaction_table,
)
