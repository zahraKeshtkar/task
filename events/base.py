import dataclasses
import logging
import traceback
from typing import Callable, Dict

_logger = logging.getLogger(__name__)
class Event:
    def __init__(self, name: str):
        self.name = name

    def publish(self, sender: Callable[[str, Dict], None], access_info: Dict):
        try:
            if dataclasses.is_dataclass(self):
                event_data = {
                    'EVENT_NAME': self.name,
                    'payload': dataclasses.asdict(self),
                    'access_info': access_info,
                }
            else:
                event_data = {
                    'EVENT_NAME': self.name,
                    'payload': {},
                    'access_info': access_info,
                }

            sender(self.name, event_data)
            _logger.info(f"Event dispatched successfully: {self.name}")
        except Exception as e:
            _logger.error(f"Failed to dispatch {self.name}: {str(e)}")
            _logger.debug(traceback.format_exc())