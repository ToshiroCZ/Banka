import unittest
from src.processor.command_processor import CommandProcessor


# Fake repository a fake bankovní služba pro CommandProcessor
class FakeRepository:
    def __init__(self):
        self.data = {}

    def get_max_account(self):
        return max(self.data.keys()) if self.data else None

    def create_account(self, account):
        self.data[account] = 0

    def get_balance(self, account):
        if account not in self.data:
            raise Exception("Účet neexistuje.")
        return self.data[account]

    def update_balance(self, account, new_balance):
        if account not in self.data:
            raise Exception("Účet neexistuje.")
        self.data[account] = new_balance

    def delete_account(self, account):
        if account not in self.data:
            raise Exception("Účet neexistuje.")
        del self.data[account]

    def get_total_amount(self):
        return sum(self.data.values())

    def get_client_count(self):
        return len(self.data)


class FakeBankService:
    def __init__(self):
        self.repo = FakeRepository()

    def create_account(self):
        account = 10000 if not self.repo.data else max(self.repo.data.keys()) + 1
        self.repo.create_account(account)
        return account

    def deposit(self, account, amount):
        current = self.repo.get_balance(account)
        self.repo.update_balance(account, current + amount)

    def withdraw(self, account, amount):
        current = self.repo.get_balance(account)
        self.repo.update_balance(account, current - amount)

    def get_balance(self, account):
        return self.repo.get_balance(account)

    def remove_account(self, account):
        balance = self.repo.get_balance(account)
        if balance > 0:
            return "ER Nelze smazat bankovní účet na kterém jsou finance."
        self.repo.delete_account(account)
        return "AR"

    def get_total_amount(self):
        return self.repo.get_total_amount()

    def get_client_count(self):
        return self.repo.get_client_count()


class TestCommandProcessor(unittest.TestCase):
    def setUp(self):
        self.fake_service = FakeBankService()
        # Nastavíme bank code na "10.0.0.96"
        self.processor = CommandProcessor(self.fake_service, "10.0.0.96")

    def test_BC_command(self):
        response = self.processor.process_command("BC")
        self.assertEqual(response, "BC 10.0.0.96")

    def test_AC_command(self):
        response = self.processor.process_command("AC")
        self.assertTrue(response.startswith("AC "))


if __name__ == '__main__':
    unittest.main()
