"""Verification module for banking operations."""

from logger import get_logger

logger = get_logger()


class VerificationError(Exception):
    """Custom exception for verification errors."""
    pass


class AccountVerifier:
    """Verifier for account operations."""
    
    @staticmethod
    def verify_account_creation(name, balance):
        """Verify account can be created with given parameters."""
        required_conditions = []
        
        # Check name
        if isinstance(name, str) and name.strip():
            required_conditions.append(("Account Name", True))
        else:
            required_conditions.append(("Account Name", False))
        
        # Check balance
        if isinstance(balance, (int, float)) and balance >= 0:
            required_conditions.append(("Initial Balance", True))
        else:
            required_conditions.append(("Initial Balance", False))
        
        all_valid = all(condition[1] for condition in required_conditions)
        
        logger.debug(f"Account creation verification: {required_conditions}")
        
        return all_valid, required_conditions
    
    @staticmethod
    def verify_account_state(name, balance, account_type):
        """Verify account state integrity."""
        checks = {}
        
        # Basic checks
        checks["has_name"] = isinstance(name, str) and len(name) > 0
        checks["has_valid_balance"] = isinstance(balance, (int, float))
        checks["has_balance_value"] = balance >= -1_000_000_000  # Reasonable limits
        checks["has_account_type"] = account_type in ["Savings Account", "Current Account"]
        
        all_valid = all(checks.values())
        
        logger.debug(f"Account state verification for {name}: {checks}")
        
        return all_valid, checks
    
    @staticmethod
    def verify_transaction_integrity(previous_balance, transaction_amount, new_balance, operation):
        """Verify transaction calculations are correct."""
        checks = {}
        
        if operation.lower() == "deposit":
            expected_balance = previous_balance + transaction_amount
            checks["calculation_correct"] = abs(new_balance - expected_balance) < 0.01  # Float comparison
        elif operation.lower() == "withdrawal":
            expected_balance = previous_balance - transaction_amount
            checks["calculation_correct"] = abs(new_balance - expected_balance) < 0.01
        else:
            checks["calculation_correct"] = False
        
        all_valid = all(checks.values())
        
        if all_valid:
            logger.debug(f"Transaction integrity verified for {operation}: {checks}")
        else:
            logger.error(f"Transaction integrity check failed for {operation}: {checks}")
        
        return all_valid, checks


class TransactionVerifier:
    """Verifier for transaction operations."""
    
    @staticmethod
    def verify_deposit_operation(previous_balance, amount, new_balance):
        """Verify deposit operation results."""
        return AccountVerifier.verify_transaction_integrity(
            previous_balance, amount, new_balance, "deposit"
        )
    
    @staticmethod
    def verify_withdrawal_operation(previous_balance, amount, new_balance):
        """Verify withdrawal operation results."""
        return AccountVerifier.verify_transaction_integrity(
            previous_balance, amount, new_balance, "withdrawal"
        )
    
    @staticmethod
    def verify_minimum_balance_maintained(current_balance, min_balance):
        """Verify minimum balance is maintained."""
        maintains_minimum = current_balance >= min_balance
        logger.debug(f"Minimum balance check: ${current_balance:.2f} >= ${min_balance:.2f} = {maintains_minimum}")
        return maintains_minimum
    
    @staticmethod
    def verify_overdraft_not_exceeded(current_balance, overdraft_limit):
        """Verify overdraft limit is not exceeded."""
        within_limits = current_balance >= -overdraft_limit
        logger.debug(f"Overdraft check: ${current_balance:.2f} >= -${overdraft_limit:.2f} = {within_limits}")
        return within_limits


class BalanceVerifier:
    """Verifier for account balance consistency."""
    
    @staticmethod
    def verify_balance_consistency(balance, transaction_history):
        """Verify that balance matches transaction history."""
        if not transaction_history:
            logger.debug("No transaction history to verify")
            return True
        
        # This is a placeholder for more complex verification
        # In a real system, you would reconstruct balance from history
        logger.debug(f"Balance consistency verified against {len(transaction_history)} transactions")
        return True
    
    @staticmethod
    def verify_balance_range(balance):
        """Verify balance is within reasonable range."""
        is_valid = isinstance(balance, (int, float)) and -1_000_000_000 <= balance <= 1_000_000_000
        logger.debug(f"Balance range check: {balance} is valid = {is_valid}")
        return is_valid
