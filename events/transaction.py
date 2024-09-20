import dataclasses

from events.base import Event

@dataclasses.dataclass
class InitiateTransaction(Event):
    """
    This event should be raised whenever a transaction is initiated!
    """
    transaction_id: str
    amount: float

    def __post_init__(self):
        super().__init__(name="INITIATE_TRANSACTION")
