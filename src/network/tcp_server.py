import socketserver
import logging


class BankTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client_ip = self.client_address[0]
        logging.info(f"Připojen klient: {client_ip}")
        try:
            # Čteme řádek po řádku
            while True:
                # readline() počká na znak nového řádku
                line_bytes = self.rfile.readline()
                if not line_bytes:
                    logging.info(f"Klient {client_ip} ukončil spojení.")
                    break  # Konec spojení

                # Dekódujeme řádek s nahrazením neplatných znaků
                line = line_bytes.decode('utf-8', errors='replace').strip()
                if not line:
                    continue  # Přeskočíme prázdné řádky

                logging.info(f"Přijat příkaz od {client_ip}: {repr(line)}")
                response = self.server.command_processor.process_command(line)
                # Logujeme odpověď – pokud začíná "ER", zalogujeme jako ERROR, jinak jako INFO
                if response.startswith("ER"):
                    logging.error(f"Odpověď pro {client_ip}: {response}")
                else:
                    logging.info(f"Odpověď pro {client_ip}: {response}")
                # Připravíme odpověď s návratem na začátek řádku a CR+LF
                full_response = "\r" + response + "\r\n"
                self.wfile.write(full_response.encode('utf-8'))
                self.wfile.flush()
        except Exception as e:
            logging.exception(f"Chyba při obsluze klienta {client_ip}: {e}")


class BankTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, command_processor):
        """
        Inicializace TCP serveru, předání command_processoru pro zpracování příkazů.
        """
        super().__init__(server_address, RequestHandlerClass)
        self.command_processor = command_processor
