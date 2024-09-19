import logging
import uuid
from decimal import Decimal
from sqlite3 import IntegrityError
from entities.transaction import TransactionEntity
from exchange.base import get_exchange_providers
from transaction import TransactionRepository
from currency import CurrencyRepository

logger = logging.getLogger(__name__)


def create_transaction(user_id: uuid.UUID, currency_id: uuid.UUID, quantity: int,
                       unit_price: Decimal) -> 'TransactionEntity':
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    if unit_price <= 0:
        raise ValueError("Unit price must be greater than 0")

    total_amount = _calculate_total_amount(unit_price, quantity)

    return TransactionEntity(
        user_id=user_id,
        currency_id=currency_id,
        count=quantity,
        amount=total_amount,
        state=TransactionEntity.TransactionState.INITIATED,
    )


def _calculate_total_amount(unit_price: Decimal, quantity: int) -> Decimal:
    return unit_price * quantity

def compute_total_cost(unit_price, quantity):
    return float(unit_price) * quantity

class TransactionManager:
    def __init__(self, user_info, currency_repo: CurrencyRepository, transaction_repo: TransactionRepository, event_publisher):
        self.user_info = user_info
        self.currency_repo = currency_repo
        self.transaction_repo = transaction_repo
        self.event_publisher = event_publisher

    def process_transaction(self, transaction_details):
        currency_id = transaction_details.get('currency_id')
        quantity = transaction_details.get('count')

        currency = self.currency_repo.find_currency_by_id(currency_id)
        if not currency:
            raise ValueError("Invalid currency")

        user_id = self.user_info['user']['id']

        with self.transaction_repo as repo:
            try:
                user = repo.lock_user_for_update(user_id)
                total_cost = compute_total_cost(currency.price, quantity)

                if user.wallet_balance < total_cost:
                    raise ValueError("Insufficient funds")

                user.wallet_balance -= total_cost
                repo.update_user_balance(user)

                transaction = create_transaction(user_id, currency.id, quantity, total_cost)
                repo.save_transaction(transaction)

                repo.commit()

                self._initiate_settlement()

                logger.info(f"Transaction successful for user {user_id} with total cost {total_cost}")

                return {
                    "user": user,
                    "total_cost": total_cost,
                    "currency": currency,
                }

            except IntegrityError as error:
                repo.rollback()
                logger.error(f"Transaction failed: Integrity error - {error} for user {user_id}")
                raise
            except ValueError as error:
                repo.rollback()
                logger.error(f"Transaction failed: Value error - {error} for user {user_id}")
                raise
            except Exception as error:
                repo.rollback()
                logger.error(f"Unexpected error during transaction: {error} for user {user_id}")
                raise

    def _initiate_settlement(self):
        events.SettlementTriggered().publish(
            event_dispatcher=self.event_publisher,
            user_info=self.user_info
        )

    def settle_pending_transactions(self):
        total_transactions_value = self.transaction_repo.calculate_total_pending_amount()
        if total_transactions_value < 10000:
            logger.warning(f"Settlement not triggered - total value = {total_transactions_value}")
            return

        exchange_services = get_exchange_providers()

        with self.transaction_repo as repo:
            try:
                pending_transactions = repo.fetch_locked_transactions(
                    state=TransactionEntity.TransactionState.INITIATED,
                )

                if not pending_transactions:
                    logger.info("No pending transactions to settle")
                    return

                transaction_ids = [tx.id for tx in pending_transactions]
                total_value_to_settle = sum(tx.amount for tx in pending_transactions)

                repo.update_transactions_to_in_progress(transaction_ids)

                for exchange_service_class in exchange_services:
                    exchange_service = exchange_service_class()
                    if exchange_service.is_available():
                        auth_token = exchange_service.request_token(user="", password="")
                        exchange_service.execute_purchase(auth_token=auth_token, amount=total_value_to_settle)
                        break

                repo.mark_transactions_as_completed(transaction_ids)
                logger.info(f"Transactions settled: {transaction_ids}")

            except Exception as error:
                logger.error(f"Error during transaction settlement: {error}")
                raise
