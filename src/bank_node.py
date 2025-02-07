import argparse
import logging
import socket
import sys

# Interní moduly
from src.network.tcp_server import BankTCPServer, BankTCPHandler
from src.processor.command_processor import CommandProcessor
from src.service.bank_service import BankService
from src.repository.bank_repository import BankRepository
from src.log import logger_config
from src.config_manager import ConfigManager

# Nastavení loggeru
logger = logger_config.setup_logger(log_filename='bank.log', log_level=logging.INFO)


def get_main_ip():
    """
    Vrátí IP adresu z hlavní sítě (např. 10.x.x.x, 192.168.x.x, 172.x.x.x),
    ignoruje localhost a VirtualBox Host-Only adresy.
    """
    ip_list = []
    try:
        hostname = socket.gethostname()
        addrinfo = socket.getaddrinfo(hostname, None)
        for info in addrinfo:
            ip = info[4][0]
            if ip.startswith("127."):
                continue
            if ip.startswith("192.168.56."):
                continue
            if ip.startswith("10.") or ip.startswith("192.168.") or ip.startswith("172."):
                ip_list.append(ip)
        if ip_list:
            return ip_list[0]
    except Exception as e:
        logger.error(f"Chyba při zjišťování IP: {e}")
    return "127.0.0.1"


def main():
    parser = argparse.ArgumentParser(description="Bankovní P2P node")
    parser.add_argument("--config", type=str, help="Cesta ke konfiguračnímu souboru (JSON)")
    parser.add_argument("--port", type=int, help="Port pro naslouchání (65525-65535)")
    parser.add_argument("--bankcode", type=str, help="IP adresa této banky; pokud není zadána,"
                                                     "automaticky se zjistí správná adresa.")
    parser.add_argument("--conn-string", type=str, default=None, help="ODBC connection string pro MSSQL")
    args = parser.parse_args()

    # Načtení konfigurace ze souboru, pokud je zadán
    config = {}
    if args.config:
        config_manager = ConfigManager(args.config)
        config = config_manager.load_config()

    # Nastavení portu: command-line > config > default (65525)
    port = args.port if args.port is not None else config.get("port", 65525)
    if not (65525 <= port <= 65535):
        logger.error("Port musí být v rozmezí 65525 až 65535.")
        sys.exit(1)

    # Nastavení bankcode: command-line > config > automatická detekce
    if args.bankcode:
        bank_code = args.bankcode
    else:
        bank_code = config.get("bankcode", get_main_ip())
    logger.info(f"Nastaven bank code: {bank_code}")

    # Nastavení timeoutů: z config nebo výchozí hodnota 5 sekund
    response_timeout = config.get("response_timeout", 5)
    client_timeout = config.get("client_timeout", 5)

    # Nastavení connection stringu: command-line > config (musí být uveden alespoň v config)
    conn_string = args.conn_string if args.conn_string else config.get("conn-string", None)
    if not conn_string:
        logger.error("Připojovací řetězec (conn-string) není zadán ani v argumentech, ani v konfiguračním souboru.")
        sys.exit(1)

    # Inicializace databázové vrstvy, obchodní logiky a zpracování příkazů
    repository = BankRepository(conn_string)
    bank_service = BankService(repository)
    command_processor = CommandProcessor(bank_service, bank_code,
                                         response_timeout=response_timeout,
                                         client_timeout=client_timeout)

    # Spuštění TCP serveru
    server = BankTCPServer(("0.0.0.0", port), BankTCPHandler, command_processor)

    try:
        logger.info(f"Server naslouchá na {port} s bankovním kódem {bank_code}")
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server byl ručně ukončen uživatelem (Ctrl+C).")
    finally:
        server.shutdown()
        server.server_close()
        logger.info("Server úspěšně ukončen.")


if __name__ == "__main__":
    main()
