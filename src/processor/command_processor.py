import logging
import socket


class CommandProcessor:
    def __init__(self, bank_service, bank_code, response_timeout=5, client_timeout=5):
        self.bank_service = bank_service
        self.bank_code = bank_code
        self.response_timeout = response_timeout
        self.client_timeout = client_timeout

    def process_command(self, command_line):
        """
        Zpracuje jeden příkaz a vrátí odpověď dle specifikace.
        """
        try:
            parts = command_line.strip().split()
            if not parts:
                return "ER Neplatný příkaz."
            cmd = parts[0].upper()

            if cmd == "BC":
                return f"BC {self.bank_code}"

            elif cmd == "AC":
                if len(parts) != 1:
                    return "ER Nesprávný formát příkazu AC."
                new_account = self.bank_service.create_account()
                return f"AC {new_account}/{self.bank_code}"

            elif cmd in ("AD", "AW", "AB"):
                account_field = None
                amount_field = None
                if cmd in ("AD", "AW"):
                    if len(parts) != 3:
                        return f"ER Nesprávný formát příkazu {cmd}."
                    account_field = parts[1]
                    amount_field = parts[2]
                else:  # AB
                    if len(parts) != 2:
                        return "ER Nesprávný formát příkazu AB."
                    account_field = parts[1]

                if '/' not in account_field:
                    return "ER Formát čísla účtu není správný."
                account_str, bank_code = account_field.split('/', 1)
                try:
                    account = int(account_str)
                except ValueError:
                    return "ER Číslo účtu není číslo."

                if bank_code != self.bank_code:
                    return self.send_command_to_remote_bank(command_line, bank_code)

                if cmd == "AD":
                    try:
                        amount = int(amount_field)
                    except ValueError:
                        return "ER Částka není ve správném formátu."
                    self.bank_service.deposit(account, amount)
                    return "AD"
                elif cmd == "AW":
                    try:
                        amount = int(amount_field)
                    except ValueError:
                        return "ER Částka není ve správném formátu."
                    self.bank_service.withdraw(account, amount)
                    return "AW"
                elif cmd == "AB":
                    balance = self.bank_service.get_balance(account)
                    return f"AB {balance}"

            elif cmd == "AR":
                if len(parts) != 2:
                    return "ER Nesprávný formát příkazu AR."
                account_field = parts[1]
                if '/' not in account_field:
                    return "ER Formát čísla účtu není správný."
                account_str, bank_code = account_field.split('/', 1)
                try:
                    account = int(account_str)
                except ValueError:
                    return "ER Číslo účtu není číslo."
                if bank_code != self.bank_code:
                    return "ER Požadavek musíte vyřešit v dané bance."
                return self.bank_service.remove_account(account)

            elif cmd == "BA":
                if len(parts) != 1:
                    return "ER Nesprávný formát příkazu BA."
                total = self.bank_service.get_total_amount()
                return f"BA {total}"

            elif cmd == "BN":
                if len(parts) != 1:
                    return "ER Nesprávný formát příkazu BN."
                count = self.bank_service.get_client_count()
                return f"BN {count}"

            else:
                return "ER Neznámý příkaz."
        except Exception as e:
            logging.error(f"Výjimka při zpracování příkazu: {str(e)}")
            return f"ER {str(e)}"

    def send_command_to_remote_bank(self, command, bank_code):
        """
        Přepošle příkaz na jinou banku (jiný uzel v P2P síti) a vrátí odpověď.
        """
        try:
            logging.info(f"Přeposílám příkaz na banku {bank_code}: {command}")
            with socket.create_connection((bank_code, 65525), timeout=self.response_timeout) as sock:
                command = command.strip() + "\n"  # Zajistíme, že příkaz končí newline
                sock.sendall(command.encode('utf-8'))
                response = sock.recv(1024).decode('utf-8').strip()
                logging.info(f"Odpověď od banky {bank_code}: {response}")
                return response
        except socket.timeout:
            logging.error(f" Timeout: Banka {bank_code} nereaguje na portu 65525.")
            return "ER Nelze se připojit k jiné bance (timeout)."
        except ConnectionRefusedError:
            logging.error(f" Spojení odmítnuto: Banka {bank_code} neběží nebo je firewall aktivní.")
            return "ER Nelze se připojit k jiné bance (odmítnuto)."
        except Exception as e:
            logging.error(f" Jiná chyba při komunikaci s bankou {bank_code}: {e}")
            return "ER Nelze se připojit k jiné bance."
