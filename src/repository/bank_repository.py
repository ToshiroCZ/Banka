import pyodbc
import threading
import logging


class BankRepository:
    def __init__(self, conn_string):
        """
        Inicializace připojení k MSSQL databázi pomocí pyodbc.
        :param conn_string: ODBC connection string.
        """
        self.conn_string = conn_string
        self.lock = threading.Lock()
        try:
            self.conn = pyodbc.connect(self.conn_string, autocommit=True)
            logging.info("Připojeno k MSSQL databázi.")
        except Exception as e:
            logging.error("Chyba při připojení k MSSQL databázi: " + str(e))
            raise
        self._initialize_db()

    def _initialize_db(self):
        """
        Vytvoří tabulku Accounts, pokud ještě neexistuje.
        """
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Accounts')
                BEGIN
                    CREATE TABLE Accounts (
                        account INT PRIMARY KEY,
                        balance BIGINT NOT NULL
                    )
                END
            """)
            cursor.commit()
            logging.info("Databáze inicializována (tabulka Accounts).")

    def create_account(self, new_account):
        """
        Vloží nový účet s daným číslem a počátečním zůstatkem 0.
        :param new_account: Číslo účtu.
        """
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Accounts (account, balance) VALUES (?, ?)", new_account, 0)
            cursor.commit()
            logging.info(f"Účet {new_account} vytvořen v databázi.")

    def get_max_account(self):
        """
        Vrací maximální číslo účtu, nebo None, pokud žádný účet zatím není.
        """
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT MAX(account) FROM Accounts")
            row = cursor.fetchone()
            return row[0] if row and row[0] is not None else None

    def update_balance(self, account, new_balance):
        """
        Aktualizuje zůstatek daného účtu.
        """
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE Accounts SET balance = ? WHERE account = ?", new_balance, account)
            if cursor.rowcount == 0:
                raise Exception("Číslo bankovního účtu neexistuje.")
            cursor.commit()
            logging.info(f"Účet {account} aktualizován, nový zůstatek: {new_balance}.")

    def get_balance(self, account):
        """
        Vrací aktuální zůstatek daného účtu.
        """
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT balance FROM Accounts WHERE account = ?", account)
            row = cursor.fetchone()
            if row is None:
                raise Exception("Číslo bankovního účtu neexistuje.")
            return row[0]

    def delete_account(self, account):
        """
        Smaže účet z databáze.
        """
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Accounts WHERE account = ?", account)
            if cursor.rowcount == 0:
                raise Exception("Číslo bankovního účtu neexistuje.")
            cursor.commit()
            logging.info(f"Účet {account} smazán z databáze.")

    def get_total_amount(self):
        """
        Vrací celkový součet zůstatků všech účtů.
        """
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT SUM(balance) FROM Accounts")
            row = cursor.fetchone()
            return row[0] if row[0] is not None else 0

    def get_client_count(self):
        """
        Vrací počet účtů (klientů) v databázi.
        """
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Accounts")
            row = cursor.fetchone()
            return row[0]