import unittest
from src.service.bank_service import BankService

class FakeRepository:
    """Fake repository pro testování bez skutečného připojení k databázi."""
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

class TestBankService(unittest.TestCase):
    def setUp(self):
        self.repo = FakeRepository()
        self.service = BankService(self.repo)

    def test_create_account(self):
        account1 = self.service.create_account()
        self.assertEqual(account1, 10000)
        account2 = self.service.create_account()
        self.assertEqual(account2, 10001)

    def test_deposit_withdraw(self):
        account = self.service.create_account()
        self.service.deposit(account, 500)
        self.assertEqual(self.service.get_balance(account), 500)
        self.service.withdraw(account, 200)
        self.assertEqual(self.service.get_balance(account), 300)
        with self.assertRaises(Exception):
            self.service.withdraw(account, 500)

    def test_remove_account(self):
        account = self.service.create_account()
        self.service.deposit(account, 100)
        with self.assertRaises(Exception):
            self.service.remove_account(account)
        self.service.withdraw(account, 100)
        self.service.remove_account(account)
        with self.assertRaises(Exception):
            self.service.get_balance(account)

if __name__ == '__main__':
    unittest.main()