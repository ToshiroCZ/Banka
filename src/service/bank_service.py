# BankService: Obchodní logika banky
# ----------------------------
import logging


class BankService:
    def __init__(self, repository):
        self.repository = repository
        # Účty musí být v rozsahu 10000 až 99999
        self.ACCOUNT_MIN = 10000
        self.ACCOUNT_MAX = 99999

    def create_account(self):
        """
        Vytvoří nový účet s unikátním číslem.
        """
        max_account = self.repository.get_max_account()
        if max_account is None:
            new_account = self.ACCOUNT_MIN
        else:
            new_account = max_account + 1
        if new_account > self.ACCOUNT_MAX:
            raise Exception("Naše banka nyní neumožňuje založení nového účtu.")
        self.repository.create_account(new_account)
        return new_account

    def deposit(self, account, amount):
        """
        Vloží peníze na účet.
        """
        if amount < 0:
            raise Exception("Částka musí být nezáporné číslo.")
        current_balance = self.repository.get_balance(account)
        new_balance = current_balance + amount
        self.repository.update_balance(account, new_balance)

    def withdraw(self, account, amount):
        """
        Vybere peníze z účtu.
        """
        if amount < 0:
            raise Exception("Částka musí být nezáporné číslo.")
        current_balance = self.repository.get_balance(account)
        if current_balance < amount:
            raise Exception("Není dostatek finančních prostředků.")
        new_balance = current_balance - amount
        self.repository.update_balance(account, new_balance)

    def get_balance(self, account):
        """
        Vrací aktuální zůstatek účtu.
        """
        return self.repository.get_balance(account)

    def remove_account(self, account):
        balance = self.repository.get_balance(account)
        if balance > 0:
            return "ER Nelze smazat bankovní účet na kterém jsou finance."
            logging.error("Chyba při zpracování příkazu '{line}': {response}")
        self.repository.delete_account(account)
        return "AR"

    def get_total_amount(self):
        """
        Vrací celkový součet zůstatků.
        """
        return self.repository.get_total_amount()

    def get_client_count(self):
        """
        Vrací počet účtů (klientů).
        """
        return self.repository.get_client_count()