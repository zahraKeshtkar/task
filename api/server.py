import json
import logging

from nameko.events import EventDispatcher, event_handler
from nameko.timer import timer
from nameko_sqlalchemy import Database
from nameko.web.handlers import http

from api.request_schema import SubmitTransactionSchema
from api.response_schema import CurrencySchema, TransactionSchema
from models.base import DeclarativeBase

from services.currency import CurrencyService
from repositories.currency import CurrencyRepository

from services.transaction import TransactionManager
from repositories.transaction import TransactionRepository
from utilities.memory import MemoryStore

_logger = logging.getLogger(__name__)


class Server:
    memory_cache = MemoryStore()
    database = Database(DeclarativeBase, engine_options={
        'pool_pre_ping': True,
        'pool_size': 100,
        'max_overflow': 100,
    })
    event_dispatcher = EventDispatcher()

    @http('GET', '/status')
    def check_health(self):
        return 200, json.dumps({})

    @http('GET', '/currencies')
    def fetch_currencies(self, request):
        currency_service = self._build_currency_service(request.access_info)
        currency_list = currency_service.list_currencies()
        return CurrencySchema(many=True).dumps(currency_list)

    @http('POST', '/transactions')
    def initiate_transaction(self, request):
        payload = SubmitTransactionSchema().load(request.get_json())
        transaction_service = self._build_transaction_service()
        transaction_response = transaction_service.transaction_repo.create_transaction(
            transaction_data=payload,
        )
        return TransactionSchema().dumps(transaction_response)

    @event_handler('core', initiate_transaction.event_name)
    def process_exchange_settlement(self, event_payload):
        _logger.debug(f"Processing settlement event with payload: {str(event_payload)}")
        transaction_service = self._build_transaction_service()
        transaction_service.settle_pending_transactions()

    @timer(interval=3600)
    def cleanup_stuck_transactions(self):
        transaction_service = self._build_transaction_service()
        transaction_service.reset_stuck_transactions()

    def _build_currency_service(self, access_info):
        currency_repository = CurrencyRepository(self.database.Session())

        return CurrencyService(
            access_info=access_info,
            currency_repo=currency_repository,
        )

    def _build_transaction_service(self):
        transaction_repository = TransactionRepository(self.database.Session())
        currency_repository = CurrencyRepository(self.database.Session())

        return TransactionManager(
            currency_repo=currency_repository,
            transaction_repo=transaction_repository,
            user_info=None,
            event_publisher=self.event_dispatcher,
        )
