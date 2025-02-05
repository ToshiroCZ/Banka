import unittest
from src.processor.command_processor import CommandProcessor
from src.service.bank_service import BankService

class FakeRepository:
    """Fake repository pro testování zpracování příkazů."""
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

class TestCommandProcessor(unittest.TestCase):
    def setUp(self):
        self.repo = FakeRepository()
        from service.bank_service import BankService  # import uvnitř, aby se nepoužíval globálně
        self.service = BankService(self.repo)
        self.processor = CommandProcessor(self.service, "127.0.0.1")

    def test_BC(self):
        self.assertEqual(self.processor.process_command("BC"), "BC 127.0.0.1")

    def test_AC(self):
        response = self.processor.process_command("AC")
        self.assertTrue(response.startswith("AC "))

    def test_AD_and_AB(self):
        ac_response = self.processor.process_command("AC")
        account = int(ac_response.split()[1].split('/')[0])
        ad_response = self.processor.process_command(f"AD {account}/127.0.0.1 1000")
        self.assertEqual(ad_response, "AD")
        ab_response = self.processor.process_command(f"AB {account}/127.0.0.1")
        self.assertEqual(ab_response, "AB 1000")

    def test_AW(self):
        ac_response = self.processor.process_command("AC")
        account = int(ac_response.split()[1].split('/')[0])
        self.processor.process_command(f"AD {account}/127.0.0.1 1000")
        aw_response = self.processor.process_command(f"AW {account}/127.0.0.1 500")
        self.assertEqual(aw_response, "AW")

    def test_AR(self):
        ac_response = self.processor.process_command("AC")
        account = int(ac_response.split()[1].split('/')[0])
        ar_response = self.processor.process_command(f"AR {account}/127.0.0.1")
        self.assertEqual(ar_response, "AR")

if __name__ == '__main__':
    unittest.main()