import socketserver
import logging
import socket


class BankTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client_ip = self.client_address[0]
        logging.info(f"Připojen klient: {client_ip}")
        try:
            # Timeout pro obsluhu klienta
            self.request.settimeout(30)

            while True:
                try:
                    line_bytes = self.rfile.readline()
                    if not line_bytes:
                        logging.info(f"Klient {client_ip} ukončil spojení.")
                        break

                    line = line_bytes.decode('utf-8', errors='replace').strip()
                    if not line:
                        continue

                    logging.info(f"Přijat příkaz od {client_ip}: {repr(line)}")
                    response = self.server.command_processor.process_command(line)

                    # Logování odpovědi (ERROR pokud začíná ER, jinak INFO)
                    if response.startswith("ER"):
                        logging.error(f"Odpověď pro {client_ip}: {response}")
                    else:
                        logging.info(f"Odpověď pro {client_ip}: {response}")

                    full_response = "\r" + response + "\r\n"
                    self.wfile.write(full_response.encode('utf-8'))
                    self.wfile.flush()
                except socket.timeout:
                    logging.error(f"Chyba při obsluze klienta {client_ip}: timed out")
                    break  # Ukončí smyčku, aby se spojení zavřelo
        except Exception as e:
            logging.error(f"Chyba při obsluze klienta {client_ip}: {e}")


class BankTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, command_processor):
        super().__init__(server_address, RequestHandlerClass)
        self.command_processor = command_processor
