from sqlalchemy import Table, Column, String, Numeric
from sqlalchemy.orm import mapper

from entities.user import UserEntity
from models.base import uuid_pk_column, temporal_columns, meta

users_table = Table(
    'users', meta,
    uuid_pk_column(),
    Column('national_number', String(255), nullable=True, unique=True),
    Column('password', String(255), nullable=False),
    Column('first_name', String(32), nullable=True),
    Column('last_name', String(32), nullable=True),
    Column('wallet_balance', Numeric(precision=12, scale=2), nullable=False, default='0.00'),
    *temporal_columns()
)

mapper(
    UserEntity,
    users_table,
)
