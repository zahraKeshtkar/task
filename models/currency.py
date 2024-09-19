from sqlalchemy import Table, Column, String, Numeric
from sqlalchemy.orm import mapper

from entities.currency import CurrencyEntity
from models.base import uuid_pk_column, meta, temporal_columns

currencies_table = Table(
    'currencies', meta,
    uuid_pk_column(),
    Column('title', String(255), nullable=False),
    Column('price', Numeric(precision=10, scale=2), nullable=True, default=None),
    *temporal_columns()
)

mapper(
    CurrencyEntity,
    currencies_table,
)
