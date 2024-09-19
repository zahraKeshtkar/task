import abc


class ExchangeServiceBase(abc.ABC):
    @abc.abstractmethod
    def authenticate_user(self, user_id, user_secret):
        """Authenticate the user and return an access token."""
        raise NotImplementedError

    @abc.abstractmethod
    def execute_purchase(self, auth_token, purchase_amount):
        """Perform a purchase operation on the exchange."""
        raise NotImplementedError

    @abc.abstractmethod
    def check_service_status(self, *args, **kwargs):
        """Check if the exchange service is operational."""
        raise NotImplementedError

def get_sorted_services():
    """Return a sorted list of available exchange services by priority."""
    subclasses = ExchangeServiceBase.__subclasses__()

    sorted_services = sorted(
        subclasses,
        key=lambda cls: getattr(cls, 'priority', float('inf'))
    )

    return sorted_services
