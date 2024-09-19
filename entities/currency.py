import datetime
import typing
import uuid
from dataclasses import dataclass, field
from decimal import Decimal

from entities.base import now

@dataclass
class CurrencyEntity:
    title: str
    price: Decimal
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = field(default_factory=now)
    updated_at: datetime.datetime = field(default_factory=now)
    deleted_at: typing.Optional[datetime.datetime] = None
