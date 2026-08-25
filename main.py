"""
Trading Operating System (TOS)

Application entry point.
"""

from __future__ import annotations

import logging
import signal
import sys
import time

from config.runtime_config_loader import RuntimeConfigLoader
from runtime.application import Application
from runtime.shutdown import Shutdown
from runtime.signal_handler import SignalHandler
from runtime.startup import Startup
from services.telegram_notifier import TelegramNotifier

LOGGER = logging.getLogger("tos")


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def create_application() -> Application:
    return Application()


def startup(app: Application) -> Startup:
    loader = RuntimeConfigLoader()
    config = loader.load()

    startup = Startup(config)

    LOGGER.info("Initializing services...")
    startup.initialize_services()

    app.services.update(startup.services)

    app.start()

    LOGGER.info("Application started.")

    return startup


def graceful_shutdown(
    app: Application,
    notifier: TelegramNotifier,
) -> None:
    LOGGER.info("Shutting down application...")

    shutdown = Shutdown()

    shutdown.save_state()
    shutdown.flush_logs()
    shutdown.close_broker()

    app.shutdown()

    notifier.send("🔴 TOS STOPPED\nTOS shutdown completed.")

    LOGGER.info("Shutdown complete.")


def register_signal_handlers(
    app: Application,
    handler: SignalHandler,
    notifier: TelegramNotifier,
) -> None:
    def _shutdown(signum, frame):
        if handler.is_shutdown_requested():
            return

        handler.register(signal.Signals(signum).name)

        graceful_shutdown(
            app,
            notifier,
        )

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)


def main() -> int:
    configure_logging()

    notifier = TelegramNotifier()

    LOGGER.info("Starting Trading Operating System...")

    app = create_application()
    signal_handler = SignalHandler()

    register_signal_handlers(
        app,
        signal_handler,
        notifier,
    )

    startup(app)

    notifier.send("🟢 TOS STARTED\nMarket: NIFTY\nMode: PAPER")

    trading_runtime = app.services["trading_runtime"]
    trading_runtime.start()

    try:
        while app.running:
            time.sleep(0.1)

    except KeyboardInterrupt:
        graceful_shutdown(
            app,
            notifier,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
