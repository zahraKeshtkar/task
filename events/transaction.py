import dataclasses

from events.base import Event

@dataclasses.dataclass
class InitiateTransaction(Event):
    transaction_id: str
    amount: float

    def __post_init__(self):
        super().__init__(name="INITIATE_TRANSACTION")
