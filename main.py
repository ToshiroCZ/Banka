import argparse
import socket
import sys
import unittest
import logging


# Hlavní funkce – spuštění serveru či testů
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="Bankovní P2P node - verze μ – mí s MSSQL a Python")
    parser.add_argument("--port", type=int, default=65525, help="Port pro naslouchání (65525-65535)")
    parser.add_argument("--bankcode", type=str, default=None, help="IP adresa této banky; pokud není zadána, automaticky se zjistí")
    parser.add_argument("--conn-string", type=str, required=True,
                        help="ODBC connection string pro MSSQL, např.: \"DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=your_db;UID=your_user;PWD=your_password\"")
    parser.add_argument("--run-tests", action="store_true", help="Spustí unit testy a ukončí aplikaci")
    args = parser.parse_args()

    # Spuštění testů, pokud je požadováno
    if args.run_tests:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestBankService)
        suite2 = unittest.TestLoader().loadTestsFromTestCase(TestCommandProcessor)
        all_tests = unittest.TestSuite([suite, suite2])
        unittest.TextTestRunner(verbosity=2).run(all_tests)
        sys.exit(0)

    if not (65525 <= args.port <= 65535):
        logging.error("Port musí být v rozmezí 65525 až 65535.")
        sys.exit(1)

    # Zjištění bank code
    if args.bankcode:
        bank_code = args.bankcode
    else:
        bank_code = socket.gethostbyname(socket.gethostname())
        logging.info(f"Nastaven bank code: {bank_code}")

    # Inicializace repository a obchodní logiky
    try:
        repository = BankRepository(args.conn_string)
    except Exception as e:
        logging.error("Nelze inicializovat BankRepository: " + str(e))
        sys.exit(1)
    bank_service = BankService(repository)
    command_processor = CommandProcessor(bank_service, bank_code)

    # Spuštění TCP serveru
    server_address = ("", args.port)
    with BankTCPServer(server_address, BankTCPHandler, command_processor) as server:
        logging.info(f"Server naslouchá na portu {args.port} (bank code: {bank_code})")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logging.info("Server byl ukončen.")

if __name__ == "__main__":
    main()