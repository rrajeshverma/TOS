from config.config_manager import ConfigManager
from config.validators import (
    validate_required,
)


class BrokerValidator:
    VALID_BROKERS = {
        "DHAN",
        "DELTA",
        "ZERODHA",
        "PAPER",
    }

    def __init__(self, manager: ConfigManager):
        self.manager = manager

    def validate(self):
        broker = self.manager.get("broker")
        validate_required(broker)

        name = self.manager.get("broker.name")
        validate_required(name)

        api_key = self.manager.get("broker.api_key")
        validate_required(api_key)

        client_id = self.manager.get("broker.client_id")
        validate_required(client_id)

        access_token = self.manager.get("broker.access_token")
        validate_required(access_token)

        if name not in self.VALID_BROKERS:
            raise ValueError(f"Unsupported broker: {name}")

        return True
