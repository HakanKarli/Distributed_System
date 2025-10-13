import logging
import multiprocessing
import time

from src.client import run_client
from src.server import run_server


def main() -> None:
    """Starte den Server und Client in separaten Prozessen."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
    )
    host = "127.0.0.1"
    port = 50_007
    message = "Hallo vom Client!"

    # Prozesse für Server und Client anlegen.
    server_process = multiprocessing.Process(target=run_server, args=(host, port))
    client_process = multiprocessing.Process(
        target=run_client, args=(host, port, message)
    )

    server_process.start()
    # Server kurz Zeit geben, den Port zu binden.
    time.sleep(0.2)
    client_process.start()

    client_process.join()
    server_process.join()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
