import datetime
import typing
import uuid
from dataclasses import dataclass, field
from decimal import Decimal

def now():
    return datetime.datetime.now(tz=datetime.timezone.utc)

@dataclass
class UserEntity:
    phone: str
    password: str
    first_name: str
    last_name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    wallet_balance: Decimal = Decimal('0.0')
    created_at: datetime.datetime = field(default_factory=now)
    updated_at: datetime.datetime = field(default_factory=now)
    deleted_at: typing.Optional[datetime.datetime] = None

