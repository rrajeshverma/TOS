class EngineRunner:
    """
    Coordinates the core runtime components of the Trading Operating System.
    """

    def __init__(self):
        self.running = False
        self.cycles = 0

        self.broker = None
        self.execution_engine = None
        self.trading_service = None
        self.runtime_state = None
        self.health_monitor = None

    # ---------------------------------------------------------
    # Dependency Injection
    # ---------------------------------------------------------

    def set_broker(self, broker):
        self.broker = broker

    def set_execution_engine(self, execution_engine):
        self.execution_engine = execution_engine

    def set_trading_service(self, trading_service):
        self.trading_service = trading_service

    def set_runtime_state(self, runtime_state):
        self.runtime_state = runtime_state

    def set_health_monitor(self, health_monitor):
        self.health_monitor = health_monitor

    # ---------------------------------------------------------
    # Broker Lifecycle
    # ---------------------------------------------------------

    def connect_broker(self):
        if self.broker:
            self.broker.connect()

    def disconnect_broker(self):
        if self.broker:
            self.broker.disconnect()

    def reconnect_broker(self):
        self.disconnect_broker()
        self.connect_broker()

    def broker_connected(self):
        if self.broker is None:
            return False

        return self.broker.is_connected()

    # ---------------------------------------------------------
    # Runtime Readiness
    # ---------------------------------------------------------

    def is_ready(self):
        return all(
            [
                self.broker is not None,
                self.execution_engine is not None,
                self.trading_service is not None,
            ]
        )

    def can_start(self):
        return self.is_ready()

    # ---------------------------------------------------------
    # Runtime Control
    # ---------------------------------------------------------

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def restart(self):
        self.stop()
        self.start()

    def shutdown(self):
        self.stop()
        self.disconnect_broker()

    def run_cycle(self):
        self.cycles += 1

    def is_running(self):
        return self.running
