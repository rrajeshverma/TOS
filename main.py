"""
Trading Operating System (TOS)

Application entry point.
"""

from __future__ import annotations

import logging
import signal
import sys

from runtime.application import Application
from runtime.startup import Startup
from runtime.shutdown import Shutdown
from runtime.signal_handler import SignalHandler


LOGGER = logging.getLogger("tos")


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def create_application() -> Application:
    app = Application()
    return app


def startup(app: Application) -> Startup:
    startup = Startup()

    LOGGER.info("Initializing services...")
    startup.initialize_services()

    app.start()

    LOGGER.info("Application started.")

    return startup


def graceful_shutdown(app: Application) -> None:
    LOGGER.info("Shutting down application...")

    shutdown = Shutdown()

    shutdown.save_state()
    shutdown.flush_logs()
    shutdown.close_broker()

    app.shutdown()

    LOGGER.info("Shutdown complete.")


def register_signal_handlers(
    app: Application,
    handler: SignalHandler,
) -> None:
    def _shutdown(signum, frame):
        handler.register(signal.Signals(signum).name)
        graceful_shutdown(app)
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)


def main() -> int:
    configure_logging()

    LOGGER.info("Starting Trading Operating System...")

    app = create_application()

    signal_handler = SignalHandler()

    register_signal_handlers(app, signal_handler)

    startup(app)

    try:
        while app.running:
            pass

    except KeyboardInterrupt:
        graceful_shutdown(app)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
