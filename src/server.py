"""Minimaler TCP-Server für einen einfachen Nachrichtentausch."""

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


class TCPServer:
    """Wartet auf einen Client, liest eine Nachricht und antwortet."""

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.logger = logging.getLogger(self.__class__.__name__)

    @log_action("Server wird gestartet.")
    def serve_once(self) -> None:
        """Startet den Server und bearbeitet genau eine Verbindung."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)
            # Server wartet auf einen eingehenden Client.
            self.logger.info("Warte auf %s:%s", self.host, self.port)

            client_socket, client_address = server_socket.accept()
            with client_socket:
                # Sobald sich ein Client verbindet, werden Daten gelesen.
                self._handle_client(client_socket, client_address)

    @log_action("Nachricht vom Client wird verarbeitet.")
    def _handle_client(self, client_socket: socket.socket, client_address) -> None:
        """Empfängt die Nachricht des Clients und sendet eine Antwort."""
        self.logger.info("Verbindung aufgebaut: %s", client_address)
        data = client_socket.recv(BUFFER_SIZE)
        message = data.decode("utf-8")
        self.logger.info("Nachricht erhalten: %s", message)
        # Antwort mit einfachem Präfix zurücksenden.
        response = f"Antwort vom Server: {message}".encode("utf-8")
        client_socket.sendall(response)
        self.logger.info("Verbindung wird geschlossen")


def run_server(host: str, port: int) -> None:
    """Hilfsfunktion für ``multiprocessing`` zum Starten des Servers."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
    )
    TCPServer(host, port).serve_once()
