# Distributed_System

TCP-Client und -Server, die in getrennten Prozessen laufen und eine Nachricht austauschen.

## Struktur
- `main.py` startet beide Prozesse.
- `src/server.py` enthält den Server mit Logging.
- `src/client.py` enthält den Client mit Logging.

## Ausführen
Mit einer Python-Installation genügt der Aufruf:

```bash
python main.py
```

Die Konsole zeigt anschließend die Logausgaben von Server und Client.
