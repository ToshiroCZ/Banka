class BankService:
    def __init__(self, repository):
        self.repository = repository
        self.ACCOUNT_MIN = 10000
        self.ACCOUNT_MAX = 99999

    def create_account(self):
        max_account = self.repository.get_max_account()
        new_account = self.ACCOUNT_MIN if max_account is None else max_account + 1
        if new_account > self.ACCOUNT_MAX:
            raise Exception("Naše banka nyní neumožňuje založení nového účtu.")
        self.repository.create_account(new_account)
        return new_account

    def deposit(self, account, amount):
        if amount < 0:
            raise Exception("Částka musí být nezáporné číslo.")
        current_balance = self.repository.get_balance(account)
        new_balance = current_balance + amount
        self.repository.update_balance(account, new_balance)

    def withdraw(self, account, amount):
        if amount < 0:
            raise Exception("Částka musí být nezáporné číslo.")
        current_balance = self.repository.get_balance(account)
        if current_balance < amount:
            raise Exception("Není dostatek finančních prostředků.")
        new_balance = current_balance - amount
        self.repository.update_balance(account, new_balance)

    def get_balance(self, account):
        return self.repository.get_balance(account)

    def remove_account(self, account):
        balance = self.repository.get_balance(account)
        if balance > 0:
            return "ER Nelze smazat bankovní účet na kterém jsou finance."
        self.repository.delete_account(account)
        return "AR"

    def get_total_amount(self):
        return self.repository.get_total_amount()

    def get_client_count(self):
        return self.repository.get_client_count()
