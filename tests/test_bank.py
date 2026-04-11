import unittest
from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount

class TestBankAccountRules(unittest.TestCase):

    def setUp(self):
        """Runs before every individual test to provide fresh objects."""
        self.savings = SavingsAccount("TestSavings", 1000)
        self.current = CurrentAccount("TestCurrent", 1000)

    # --- SAVINGS ACCOUNT TESTS ---

    def test_savings_min_balance_rule(self):
        """Verify Savings cannot drop below $500."""
        # Attempt to withdraw $600 (leaves $400, which is < $500)
        result = self.savings.withdraw(600)
        self.assertFalse(result, "Savings should block withdrawal below $500")
        self.assertEqual(self.savings.get_balance(), 1000, "Balance should remain unchanged")

    def test_savings_valid_withdrawal(self):
        """Verify Savings allows withdrawal if above $500."""
        result = self.savings.withdraw(200)
        self.assertTrue(result)
        self.assertEqual(self.savings.get_balance(), 800)

    # --- CURRENT ACCOUNT TESTS ---

    def test_current_overdraft_limit(self):
        """Verify Current allows overdraft up to $1000."""
        # Balance is $1000. Withdraw $1500 (Result: -$500). Limit is -$1000.
        result = self.current.withdraw(1500)
        self.assertTrue(result, "Current should allow overdraft within limit")
        self.assertEqual(self.current.get_balance(), -500)

    def test_current_exceed_overdraft(self):
        """Verify Current blocks withdrawal beyond -$1000."""
        # Balance is $1000. Withdraw $2500 (Result: -$1500). Limit is -$1000.
        result = self.current.withdraw(2500)
        self.assertFalse(result, "Current should block withdrawal exceeding overdraft limit")
        self.assertEqual(self.current.get_balance(), 1000)

    # --- COMMON TESTS ---

    def test_deposit_logic(self):
        """Verify deposits increase balance correctly."""
        self.savings.deposit(500)
        self.assertEqual(self.savings.get_balance(), 1500)

if __name__ == "__main__":
    unittest.main()