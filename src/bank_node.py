# External
import argparse
import logging
import socket
import sys

# Internal
from src.network.tcp_server import BankTCPServer, BankTCPHandler
from src.processor.command_processor import CommandProcessor
from src.service.bank_service import BankService
from src.repository.bank_repository import BankRepository
from src.log import logger_config

logger = logger_config.setup_logger(log_filename='bank.log', log_level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Bankovní P2P node – verze μ – mí s MSSQL")
    parser.add_argument("--port", type=int, default=65525, help="Port pro naslouchání (65525-65535)")
    parser.add_argument("--bankcode", type=str, default=None, help="IP adresa této banky; pokud není zadána, použije se lokální IP")
    parser.add_argument("--conn-string", type=str, required=True,
                        help="ODBC connection string pro MSSQL, např.: \"DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=your_db;UID=your_user;PWD=your_password\"")
    args = parser.parse_args()

    if not (65525 <= args.port <= 65535):
        logger.error("Port musí být v rozmezí 65525 až 65535.")
        sys.exit(1)

    # Pokud bank code není zadán, zjistíme lokální IP
    if args.bankcode:
        bank_code = args.bankcode
    else:
        bank_code = socket.gethostbyname(socket.gethostname())
    logger.info(f"Nastaven bank code: {bank_code}")

    # Inicializace databázové vrstvy, obchodní logiky a zpracování příkazů
    repository = BankRepository(args.conn_string)
    bank_service = BankService(repository)
    command_processor = CommandProcessor(bank_service, bank_code)

    # Spuštění TCP serveru
    server = BankTCPServer(("0.0.0.0", args.port), BankTCPHandler, command_processor)
    logging.info(f"Server naslouchá na {args.port} s bankovním kódem {args.bankcode}")

    server.serve_forever()

if __name__ == "__main__":
    main()