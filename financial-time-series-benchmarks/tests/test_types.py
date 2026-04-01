# -*- coding: utf-8 -*-
"""
Tests for Financial Domain Types

Business Intent:
    Verify that all financial types are correctly implemented and prevent errors.
    100% coverage required for all financial logic.
"""

import pytest
from decimal import Decimal
from datetime import datetime, timezone
import warnings

from models.types import (
    MoneyValue,
    PnL,
    Return,
    Currency,
    ReturnUnit,
    create_money,
    create_return,
    PrecisionWarning,
)


class TestMoneyValue:
    """Test MoneyValue type"""
    
    def test_create_money_value(self):
        """Test basic MoneyValue creation"""
        money = MoneyValue(Decimal('1000.50'), Currency.USD)
        assert money.amount == Decimal('1000.50')
        assert money.currency == Currency.USD
        assert str(money) == "1000.50 USD"
    
    def test_create_money_value_invalid_type(self):
        """Test that invalid types are rejected"""
        with pytest.raises(TypeError):
            MoneyValue(1000.50, Currency.USD)  # Must be Decimal
        
        with pytest.raises(TypeError):
            MoneyValue(Decimal('1000.50'), 'USD')  # Must be Currency enum
    
    def test_money_addition(self):
        """Test MoneyValue addition"""
        money1 = MoneyValue(Decimal('1000.00'), Currency.USD)
        money2 = MoneyValue(Decimal('500.00'), Currency.USD)
        
        result = money1 + money2
        assert result.amount == Decimal('1500.00')
        assert result.currency == Currency.USD
    
    def test_money_addition_currency_mismatch(self):
        """Test that adding different currencies fails"""
        money1 = MoneyValue(Decimal('1000.00'), Currency.USD)
        money2 = MoneyValue(Decimal('500.00'), Currency.CNY)
        
        with pytest.raises(ValueError):
            money1 + money2
    
    def test_money_subtraction(self):
        """Test MoneyValue subtraction"""
        money1 = MoneyValue(Decimal('1000.00'), Currency.USD)
        money2 = MoneyValue(Decimal('500.00'), Currency.USD)
        
        result = money1 - money2
        assert result.amount == Decimal('500.00')
    
    def test_money_multiplication(self):
        """Test MoneyValue multiplication"""
        money = MoneyValue(Decimal('1000.00'), Currency.USD)
        result = money * Decimal('1.5')
        assert result.amount == Decimal('1500.00')


class TestPnL:
    """Test PnL type"""
    
    def test_create_pnl(self):
        """Test basic PnL creation"""
        pnl = PnL(
            amount=Decimal('150.50'),
            currency=Currency.USD,
            timestamp=datetime.now(timezone.utc),
            strategy_id='test_strategy'
        )
        
        assert pnl.amount == Decimal('150.50')
        assert pnl.is_profit()
        assert not pnl.is_loss()
    
    def test_create_pnl_loss(self):
        """Test PnL with loss"""
        pnl = PnL(
            amount=Decimal('-200.00'),
            currency=Currency.USD,
            timestamp=datetime.now(timezone.utc),
            strategy_id='test_strategy'
        )
        
        assert pnl.amount == Decimal('-200.00')
        assert pnl.is_loss()
        assert not pnl.is_profit()
    
    def test_create_pnl_invalid_timestamp(self):
        """Test that naive timestamps are rejected"""
        with pytest.raises(ValueError):
            PnL(
                amount=Decimal('100.00'),
                currency=Currency.USD,
                timestamp=datetime.now(),  # Naive timestamp
                strategy_id='test'
            )
    
    def test_create_pnl_empty_strategy(self):
        """Test that empty strategy_id is rejected"""
        with pytest.raises(ValueError):
            PnL(
                amount=Decimal('100.00'),
                currency=Currency.USD,
                timestamp=datetime.now(timezone.utc),
                strategy_id=''
            )


class TestReturn:
    """Test Return type"""
    
    def test_create_return_decimal(self):
        """Test Return with decimal unit"""
        ret = Return(Decimal('0.05'), ReturnUnit.DECIMAL)
        assert ret.to_decimal() == Decimal('0.05')
        assert ret.to_percent() == Decimal('5.0')
        assert ret.to_basis_points() == Decimal('500')
    
    def test_create_return_percent(self):
        """Test Return with percent unit"""
        ret = Return(Decimal('5.0'), ReturnUnit.PERCENT)
        assert ret.to_decimal() == Decimal('0.05')
        assert str(ret) == "5.00%"
    
    def test_create_return_basis_points(self):
        """Test Return with basis points unit"""
        ret = Return(Decimal('500'), ReturnUnit.BASIS_POINT)
        assert ret.to_decimal() == Decimal('0.05')
        assert str(ret) == "500 bp"
    
    def test_create_return_invalid_type(self):
        """Test that invalid types are rejected"""
        with pytest.raises(TypeError):
            Return(0.05, ReturnUnit.DECIMAL)  # Must be Decimal


class TestCreateMoney:
    """Test create_money helper function"""
    
    def test_create_from_decimal(self):
        """Test creating Money from Decimal"""
        money = create_money(Decimal('1000.50'), Currency.USD)
        assert money.amount == Decimal('1000.50')
    
    def test_create_from_string(self):
        """Test creating Money from string"""
        money = create_money('1000.50', Currency.USD)
        assert money.amount == Decimal('1000.50')
    
    def test_create_from_float_warns(self):
        """Test that creating Money from float warns"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            money = create_money(1000.50, Currency.USD)
            
            assert len(w) == 1
            assert issubclass(w[0].category, PrecisionWarning)
            assert "precision loss" in str(w[0].message).lower()
    
    def test_create_rounds_correctly(self):
        """Test that Money is rounded correctly"""
        money = create_money(Decimal('1000.555'), Currency.USD)
        assert money.amount == Decimal('1000.56')  # Rounded to 2 decimals


class TestCreateReturn:
    """Test create_return helper function"""
    
    def test_create_from_decimal(self):
        """Test creating Return from Decimal"""
        ret = create_return(Decimal('0.05'), ReturnUnit.DECIMAL)
        assert ret.value == Decimal('0.05')
    
    def test_create_from_float_warns(self):
        """Test that creating Return from float warns"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            ret = create_return(0.05, ReturnUnit.DECIMAL)
            
            assert len(w) == 1
            assert issubclass(w[0].category, PrecisionWarning)


class TestCurrency:
    """Test Currency enum"""
    
    def test_currency_values(self):
        """Test currency enum values"""
        assert Currency.USD.value == 'USD'
        assert Currency.CNY.value == 'CNY'
        assert Currency.EUR.value == 'EUR'


class TestReturnUnit:
    """Test ReturnUnit enum"""
    
    def test_return_unit_values(self):
        """Test return unit enum values"""
        assert ReturnUnit.DECIMAL.value == 'decimal'
        assert ReturnUnit.PERCENT.value == 'percent'
        assert ReturnUnit.BASIS_POINT.value == 'basis_point'
