"""Validation module for banking operations."""

from logger import get_logger

logger = get_logger()


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class AccountValidator:
    """Validator for account operations."""
    
    @staticmethod
    def validate_name(name):
        """Validate account holder name."""
        if not isinstance(name, str):
            error_msg = "Name must be a string."
            logger.error(error_msg)
            raise ValidationError(error_msg)
        
        if not name or len(name.strip()) == 0:
            error_msg = "Name cannot be empty."
            logger.error(error_msg)
            raise ValidationError(error_msg)
        
        if len(name) > 100:
            error_msg = "Name cannot exceed 100 characters."
            logger.error(error_msg)
            raise ValidationError(error_msg)
        
        logger.debug(f"Name validation passed: {name}")
        return True
    
    @staticmethod
    def validate_balance(balance):
        """Validate initial balance."""
        if not isinstance(balance, (int, float)):
            error_msg = "Balance must be a number."
            logger.error(error_msg)
            raise ValidationError(error_msg)
        
        if balance < 0:
            error_msg = "Initial balance cannot be negative."
            logger.error(error_msg)
            raise ValidationError(error_msg)
        
        logger.debug(f"Balance validation passed: ${balance:.2f}")
        return True
    
    @staticmethod
    def validate_amount(amount, operation=""):
        """Validate transaction amount."""
        if not isinstance(amount, (int, float)):
            error_msg = f"Amount must be a number for {operation}."
            logger.error(error_msg)
            raise ValidationError(error_msg)
        
        if amount <= 0:
            error_msg = f"Amount must be positive for {operation}."
            logger.error(error_msg)
            raise ValidationError(error_msg)
        
        if amount > 1_000_000_000:  # Reasonable upper limit
            error_msg = f"Amount exceeds maximum limit for {operation}."
            logger.error(error_msg)
            raise ValidationError(error_msg)
        
        logger.debug(f"Amount validation passed: ${amount:.2f} for {operation}")
        return True
    
    @staticmethod
    def validate_savings_withdrawal(current_balance, amount, min_balance):
        """Validate savings account withdrawal."""
        if current_balance - amount < min_balance:
            error_msg = f"Withdrawal would result in balance below minimum ${min_balance:.2f}."
            logger.warning(error_msg)
            return False, error_msg
        
        logger.debug(f"Savings withdrawal validation passed.")
        return True, "Valid"
    
    @staticmethod
    def validate_overdraft_withdrawal(current_balance, amount, overdraft_limit):
        """Validate current account withdrawal with overdraft."""
        if current_balance - amount < -overdraft_limit:
            error_msg = f"Withdrawal would exceed overdraft limit of ${overdraft_limit:.2f}."
            logger.warning(error_msg)
            return False, error_msg
        
        logger.debug(f"Overdraft withdrawal validation passed.")
        return True, "Valid"


class TransactionValidator:
    """Validator for transaction operations."""
    
    @staticmethod
    def validate_transaction_amount(amount):
        """Validate transaction amount."""
        return AccountValidator.validate_amount(amount, operation="transaction")
    
    @staticmethod
    def validate_sufficient_balance(current_balance, amount):
        """Validate sufficient balance for withdrawal."""
        if current_balance < amount:
            error_msg = f"Insufficient balance. Current: ${current_balance:.2f}, Required: ${amount:.2f}"
            logger.warning(error_msg)
            return False, error_msg
        
        return True, "Sufficient balance"
