# -*- coding: utf-8 -*-
"""
Tests for Random Seed Management

Business Intent:
    Verify that all random operations are deterministic.
    Ensure same inputs produce identical outputs.
    Enable full reproducibility for audit trail.
"""

import pytest
import numpy as np

from utils.seed import (
    set_global_seed,
    get_global_seed,
    set_component_seed,
    get_component_seed,
    get_seed_registry,
    clear_seed_registry,
    generate_seed,
    temporary_seed,
    with_seed,
)


class TestGlobalSeed:
    """Test global seed management"""
    
    def setup_method(self):
        """Reset seed registry before each test"""
        clear_seed_registry()
    
    def test_set_global_seed(self):
        """Test setting global seed"""
        set_global_seed(42)
        assert get_global_seed() == 42
    
    def test_set_global_seed_invalid_type(self):
        """Test that invalid seed type is rejected"""
        with pytest.raises(TypeError):
            set_global_seed("not_an_int")
        
        with pytest.raises(TypeError):
            set_global_seed(42.5)
    
    def test_set_global_seed_negative(self):
        """Test that negative seed is rejected"""
        with pytest.raises(ValueError):
            set_global_seed(-1)
    
    def test_global_seed_determinism(self):
        """Test that same seed produces same results"""
        # Run 1
        set_global_seed(42)
        result1 = np.random.randn(10)
        
        # Run 2
        set_global_seed(42)
        result2 = np.random.randn(10)
        
        # Assert identical
        np.testing.assert_array_equal(result1, result2)
    
    def test_different_seeds_different_results(self):
        """Test that different seeds produce different results"""
        # Run 1
        set_global_seed(42)
        result1 = np.random.randn(10)
        
        # Run 2
        set_global_seed(123)
        result2 = np.random.randn(10)
        
        # Assert different
        assert not np.array_equal(result1, result2)


class TestComponentSeed:
    """Test component-specific seed management"""
    
    def setup_method(self):
        """Reset seed registry before each test"""
        clear_seed_registry()
    
    def test_set_component_seed(self):
        """Test setting component seed"""
        set_component_seed('data_loader', 123)
        assert get_component_seed('data_loader') == 123
    
    def test_set_component_seed_invalid_component(self):
        """Test that invalid component is rejected"""
        with pytest.raises(ValueError):
            set_component_seed('', 123)
        
        with pytest.raises(ValueError):
            set_component_seed(None, 123)
    
    def test_set_component_seed_invalid_seed(self):
        """Test that invalid seed is rejected"""
        with pytest.raises(TypeError):
            set_component_seed('data_loader', "not_an_int")
        
        with pytest.raises(ValueError):
            set_component_seed('data_loader', -1)
    
    def test_component_seed_isolation(self):
        """Test that component seeds are isolated"""
        set_component_seed('data_loader', 123)
        set_component_seed('model', 456)
        
        assert get_component_seed('data_loader') == 123
        assert get_component_seed('model') == 456


class TestSeedRegistry:
    """Test seed registry"""
    
    def setup_method(self):
        """Reset seed registry before each test"""
        clear_seed_registry()
    
    def test_get_seed_registry(self):
        """Test getting complete registry"""
        set_global_seed(42)
        set_component_seed('data_loader', 123)
        set_component_seed('model', 456)
        
        registry = get_seed_registry()
        
        assert registry['global'] == 42
        assert registry['data_loader'] == 123
        assert registry['model'] == 456
    
    def test_clear_seed_registry(self):
        """Test clearing registry"""
        set_global_seed(42)
        set_component_seed('data_loader', 123)
        
        clear_seed_registry()
        
        assert get_global_seed() is None
        assert get_component_seed('data_loader') is None


class TestGenerateSeed:
    """Test seed generation"""
    
    def setup_method(self):
        """Reset seed registry before each test"""
        clear_seed_registry()
    
    def test_generate_seed(self):
        """Test seed generation"""
        seed = generate_seed()
        
        assert isinstance(seed, int)
        assert seed >= 0
        assert seed < 2**31
    
    def test_generate_seed_tracked(self):
        """Test that generated seed is tracked"""
        generate_seed()
        
        assert 'last_generated' in get_seed_registry()


class TestTemporarySeed:
    """Test temporary seed context manager"""
    
    def setup_method(self):
        """Reset seed registry before each test"""
        clear_seed_registry()
    
    def test_temporary_seed(self):
        """Test temporary seed changes"""
        set_global_seed(42)
        
        with temporary_seed(123):
            assert get_global_seed() == 123
        
        # Seed should be restored
        assert get_global_seed() == 42
    
    def test_temporary_seed_determinism(self):
        """Test that temporary seed produces deterministic results"""
        # Run 1
        with temporary_seed(42):
            result1 = np.random.randn(5)
        
        # Run 2
        with temporary_seed(42):
            result2 = np.random.randn(5)
        
        # Assert identical
        np.testing.assert_array_equal(result1, result2)
    
    def test_temporary_seed_exception_handling(self):
        """Test that seed is restored even on exception"""
        set_global_seed(42)
        
        try:
            with temporary_seed(123):
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        # Seed should still be restored
        assert get_global_seed() == 42


class TestWithSeedDecorator:
    """Test with_seed decorator"""
    
    def setup_method(self):
        """Reset seed registry before each test"""
        clear_seed_registry()
    
    def test_with_seed_decorator(self):
        """Test decorator sets seed"""
        @with_seed(42)
        def generate_random():
            return np.random.randn(5)
        
        # Run 1
        result1 = generate_random()
        
        # Run 2
        result2 = generate_random()
        
        # Assert identical
        np.testing.assert_array_equal(result1, result2)
    
    def test_with_seed_restores_seed(self):
        """Test that decorator restores seed"""
        set_global_seed(42)
        
        @with_seed(123)
        def generate_random():
            return np.random.randn(5)
        
        generate_random()
        
        # Seed should be restored
        assert get_global_seed() == 42


class TestDeterminismIntegration:
    """Test determinism in realistic scenarios"""
    
    def setup_method(self):
        """Reset seed registry before each test"""
        clear_seed_registry()
    
    def test_synthetic_data_determinism(self):
        """Test that synthetic data is deterministic"""
        from data.loader import load_stock_data
        
        # Run 1
        set_global_seed(42)
        df1 = load_stock_data('TEST', '2023-01-01', '2023-01-31', 'synthetic')
        
        # Run 2
        set_global_seed(42)
        df2 = load_stock_data('TEST', '2023-01-01', '2023-01-31', 'synthetic')
        
        # Assert identical
        import pandas as pd
        pd.testing.assert_frame_equal(df1, df2)
    
    def test_model_determinism(self):
        """Test that model predictions are deterministic"""
        from models.baseline.naive import RandomWalk
        import pandas as pd
        
        prices = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0])
        
        # Run 1
        set_global_seed(42)
        model1 = RandomWalk()
        model1.fit(prices)
        pred1 = model1.predict(steps=3)
        
        # Run 2
        set_global_seed(42)
        model2 = RandomWalk()
        model2.fit(prices)
        pred2 = model2.predict(steps=3)
        
        # Assert identical
        import numpy as np
        np.testing.assert_array_equal(pred1, pred2)
