# -*- coding: utf-8 -*-
"""
Financial Domain Types

Business Intent:
    Provide explicit, type-safe abstractions for financial values.
    Ensures numerical integrity and prevents floating-point errors in financial calculations.
    
Design Boundaries:
    - All monetary values must use Money or Decimal type
    - All prices must use Price type
    - All returns must use Return type
    - No raw floats for financial values in production code
    
Applicable Scenarios:
    - Production trading logic
    - Risk calculations
    - PnL calculations
    - Fee calculations
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Union, NewType
from dataclasses import dataclass
from enum import Enum
import datetime


# Type aliases for clarity
Money = Decimal
Price = Decimal
Return = Decimal
Quantity = Decimal


class Currency(Enum):
    """
    Currency codes (ISO 4217).
    
    Business Intent:
        Explicit currency representation to prevent currency confusion.
    """
    USD = 'USD'
    CNY = 'CNY'
    EUR = 'EUR'
    GBP = 'GBP'
    JPY = 'JPY'
    HKD = 'HKD'


@dataclass
class MoneyValue:
    """
    Explicit monetary value with currency.
    
    Business Intent:
        Prevent currency confusion and ensure precise monetary calculations.
        All monetary values in production must use this type.
    
    Attributes:
        amount: Monetary amount (Decimal for precision)
        currency: Currency code (ISO 4217)
    
    Usage:
        >>> value = MoneyValue(Decimal('1000.00'), Currency.USD)
        >>> value.amount
        Decimal('1000.00')
        >>> value.currency
        Currency.USD
    """
    amount: Decimal
    currency: Currency
    
    def __post_init__(self):
        # Fail-fast: Validate amount
        if not isinstance(self.amount, Decimal):
            raise TypeError(f"Amount must be Decimal, got {type(self.amount)}")
        
        # Fail-fast: Validate currency
        if not isinstance(self.currency, Currency):
            raise TypeError(f"Currency must be Currency enum, got {type(self.currency)}")
    
    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency.value}"
    
    def __add__(self, other: 'MoneyValue') -> 'MoneyValue':
        # Fail-fast: Currency must match
        if self.currency != other.currency:
            raise ValueError(f"Cannot add different currencies: {self.currency} vs {other.currency}")
        return MoneyValue(self.amount + other.amount, self.currency)
    
    def __sub__(self, other: 'MoneyValue') -> 'MoneyValue':
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract different currencies: {self.currency} vs {other.currency}")
        return MoneyValue(self.amount - other.amount, self.currency)
    
    def __mul__(self, factor: Decimal) -> 'MoneyValue':
        return MoneyValue(self.amount * factor, self.currency)
    
    def to_decimal(self) -> Decimal:
        """Convert to Decimal for calculations."""
        return self.amount


@dataclass
class PnL:
    """
    Profit and Loss representation.
    
    Business Intent:
        Explicit PnL tracking with currency and timestamp.
        All PnL calculations must use this type for traceability.
    
    Attributes:
        amount: PnL amount (positive for profit, negative for loss)
        currency: Currency code
        timestamp: When the PnL was realized (UTC)
        strategy_id: Which strategy generated this PnL
    
    Usage:
        >>> pnl = PnL(
        ...     amount=Decimal('150.50'),
        ...     currency=Currency.USD,
        ...     timestamp=datetime.datetime.utcnow(),
        ...     strategy_id='momentum_001'
        ... )
    """
    amount: Decimal
    currency: Currency
    timestamp: datetime.datetime
    strategy_id: str
    
    def __post_init__(self):
        # Fail-fast: Validate all fields
        if not isinstance(self.amount, Decimal):
            raise TypeError(f"Amount must be Decimal, got {type(self.amount)}")
        
        if not isinstance(self.currency, Currency):
            raise TypeError(f"Currency must be Currency enum, got {type(self.currency)}")
        
        if not isinstance(self.timestamp, datetime.datetime):
            raise TypeError(f"Timestamp must be datetime, got {type(self.timestamp)}")
        
        # Fail-fast: Timestamp must be timezone-aware
        if self.timestamp.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware (use UTC)")
        
        if not self.strategy_id:
            raise ValueError("Strategy ID cannot be empty")
    
    def is_profit(self) -> bool:
        """Check if this is a profitable trade."""
        return self.amount > 0
    
    def is_loss(self) -> bool:
        """Check if this is a losing trade."""
        return self.amount < 0
    
    def to_decimal(self) -> Decimal:
        """Convert to Decimal for calculations."""
        return self.amount


class ReturnUnit(Enum):
    """
    Return representation unit.
    
    Business Intent:
        Explicit representation of return units to prevent confusion.
    """
    DECIMAL = 'decimal'  # e.g., 0.05 for 5%
    PERCENT = 'percent'  # e.g., 5.0 for 5%
    BASIS_POINT = 'basis_point'  # e.g., 500 for 5%


@dataclass
class Return:
    """
    Return representation with explicit unit.
    
    Business Intent:
        Prevent return calculation errors due to unit confusion.
        All returns must specify their unit explicitly.
    
    Attributes:
        value: Return value
        unit: Return unit (decimal, percent, or basis_point)
    
    Usage:
        >>> ret = Return(Decimal('0.05'), ReturnUnit.DECIMAL)
        >>> ret.to_percent()
        Decimal('5.0')
        >>> ret.to_basis_points()
        Decimal('500')
    """
    value: Decimal
    unit: ReturnUnit
    
    def __post_init__(self):
        # Fail-fast: Validate inputs
        if not isinstance(self.value, Decimal):
            raise TypeError(f"Value must be Decimal, got {type(self.value)}")
        
        if not isinstance(self.unit, ReturnUnit):
            raise TypeError(f"Unit must be ReturnUnit enum, got {type(self.unit)}")
    
    def to_decimal(self) -> Decimal:
        """Convert to decimal representation (e.g., 0.05 for 5%)."""
        if self.unit == ReturnUnit.DECIMAL:
            return self.value
        elif self.unit == ReturnUnit.PERCENT:
            return self.value / Decimal('100')
        elif self.unit == ReturnUnit.BASIS_POINT:
            return self.value / Decimal('10000')
        else:
            raise ValueError(f"Unknown unit: {self.unit}")
    
    def to_percent(self) -> Decimal:
        """Convert to percent representation (e.g., 5.0 for 5%)."""
        return self.to_decimal() * Decimal('100')
    
    def to_basis_points(self) -> Decimal:
        """Convert to basis points (e.g., 500 for 5%)."""
        return self.to_decimal() * Decimal('10000')
    
    def __str__(self) -> str:
        if self.unit == ReturnUnit.DECIMAL:
            return f"{self.value:.4f}"
        elif self.unit == ReturnUnit.PERCENT:
            return f"{self.value:.2f}%"
        elif self.unit == ReturnUnit.BASIS_POINT:
            return f"{self.value:.0f} bp"
        else:
            return str(self.value)


# Helper functions for creating financial values

def create_money(amount: Union[str, int, float, Decimal], currency: Currency = Currency.USD) -> MoneyValue:
    """
    Create MoneyValue from various input types.
    
    Business Intent:
        Safe money creation with automatic Decimal conversion.
        Prevents floating-point precision errors.
    
    Args:
        amount: Amount in any numeric type (will be converted to Decimal)
        currency: Currency code (default: USD)
    
    Returns:
        MoneyValue with precise Decimal amount
    
    Usage:
        >>> money = create_money(1000.50, Currency.USD)
        >>> money.amount
        Decimal('1000.50')
    """
    # Fail-fast: Convert to Decimal safely
    if isinstance(amount, float):
        # Fail-fast: Warn about float usage
        import warnings
        warnings.warn(
            "Creating Money from float may cause precision loss. Use Decimal or str instead.",
            PrecisionWarning,
            stacklevel=2
        )
        amount = Decimal(str(amount))
    elif not isinstance(amount, Decimal):
        amount = Decimal(amount)
    
    return MoneyValue(amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), currency)


def create_return(value: Union[str, int, float, Decimal], unit: ReturnUnit = ReturnUnit.DECIMAL) -> Return:
    """
    Create Return from various input types.
    
    Business Intent:
        Safe return creation with explicit unit.
    
    Args:
        value: Return value
        unit: Return unit (default: decimal)
    
    Returns:
        Return with explicit unit
    
    Usage:
        >>> ret = create_return(0.05, ReturnUnit.DECIMAL)
        >>> ret.to_percent()
        Decimal('5.0')
    """
    if isinstance(value, float):
        import warnings
        warnings.warn(
            "Creating Return from float may cause precision loss. Use Decimal or str instead.",
            PrecisionWarning,
            stacklevel=2
        )
        value = Decimal(str(value))
    elif not isinstance(value, Decimal):
        value = Decimal(value)
    
    return Return(value, unit)


class PrecisionWarning(Warning):
    """
    Warning for potential precision loss in financial calculations.
    
    Business Intent:
        Alert developers when using imprecise types (float) for financial values.
    """
    pass
