"""Minimaler TCP-Client für einen einfachen Nachrichtentausch."""

import logging
import socket
from functools import wraps
from typing import Any, Callable, TypeVar

BUFFER_SIZE = 1024
F = TypeVar("F", bound=Callable[..., Any])


def log_action(message: str) -> Callable[[F], F]:
    """Dekorator, der vor Ausführung der Methode eine Log-Nachricht schreibt."""

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.logger.info(message)
            return func(self, *args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


class TCPClient:
    """Verbindet sich mit dem Server, sendet eine Nachricht und protokolliert die Antwort."""

    def __init__(self, host: str, port: int, message: str) -> None:
        self.host = host
        self.port = port
        self.message = message
        self.logger = logging.getLogger(self.__class__.__name__)

    @log_action("Client verbindet sich mit dem Server.")
    def exchange_messages(self) -> None:
        """Sendet ``message`` und protokolliert die Antwort des Servers."""
        # Verbindung zum Server aufbauen und Nachricht schicken.
        with socket.create_connection((self.host, self.port)) as sock:
            self.logger.info("Verbunden mit %s:%s", self.host, self.port)
            sock.sendall(self.message.encode("utf-8"))
            # Antwort lesen und anzeigen.
            data = sock.recv(BUFFER_SIZE)
            reply = data.decode("utf-8")
            self.logger.info("Antwort erhalten: %s", reply)


def run_client(host: str, port: int, message: str) -> None:
    """Hilfsfunktion für ``multiprocessing`` zum Starten des Clients."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
    )
    TCPClient(host, port, message).exchange_messages()
