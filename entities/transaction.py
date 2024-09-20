import datetime
import enum
import typing
from dataclasses import dataclass, field
import uuid
from decimal import Decimal

from entities.base import now


@dataclass
class TransactionEntity:
    class TransactionState(enum.Enum):
        INITIATED = 'Initiated'
        PROCESSING = 'Processing'
        COMPLETED = 'Completed'
    user_id: uuid.UUID
    currency_id: uuid.UUID
    count: int
    amount: Decimal
    state: TransactionState = TransactionState.INITIATED
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = field(default_factory=now)
    updated_at: datetime.datetime = field(default_factory=now)
    deleted_at: typing.Optional[datetime.datetime] = None
