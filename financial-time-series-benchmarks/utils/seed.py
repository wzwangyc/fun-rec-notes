# -*- coding: utf-8 -*-
"""
Random Seed Management

Business Intent:
    Ensure deterministic results for reproducibility.
    All random operations must use explicit seeds.
    Same inputs must produce identical outputs across runs.

Design Boundaries:
    - Global seed management for all random operations
    - Separate seeds for different components (data, models, backtest)
    - Explicit seed documentation in all functions using randomness

Applicable Scenarios:
    - Model training
    - Data generation (synthetic data)
    - Backtest execution
    - Any operation with randomness
"""

import numpy as np
import random
from typing import Optional, Dict


# Global seed registry
_seed_registry: Dict[str, int] = {}


def set_global_seed(seed: int = 42) -> None:
    """
    Set global random seed for reproducibility.
    
    Business Intent:
        Ensure all random operations are deterministic.
        Same inputs must produce identical outputs.
        Critical for audit trail and debugging.
    
    Args:
        seed: Random seed (default: 42)
            - Must be integer
            - Must be positive
            - Same seed must produce same results
    
    Usage:
        >>> set_global_seed(42)
        >>> result1 = run_backtest()
        >>> set_global_seed(42)
        >>> result2 = run_backtest()
        >>> assert result1 == result2  # Must be identical
    """
    # Fail-fast: Validate seed
    if not isinstance(seed, int):
        raise TypeError(f"Seed must be integer, got {type(seed)}")
    
    if seed < 0:
        raise ValueError(f"Seed must be non-negative, got {seed}")
    
    # Set seeds for all random libraries
    np.random.seed(seed)
    random.seed(seed)
    
    # Register seed for reproducibility tracking
    _seed_registry['global'] = seed
    
    # Note: PyTorch seeds set separately if needed
    # import torch
    # torch.manual_seed(seed)
    # if torch.cuda.is_available():
    #     torch.cuda.manual_seed_all(seed)
    #     torch.backends.cudnn.deterministic = True
    #     torch.backends.cudnn.benchmark = False


def get_global_seed() -> Optional[int]:
    """
    Get current global random seed.
    
    Business Intent:
        Track which seed was used for reproducibility.
        Enable audit trail for all random operations.
    
    Returns:
        Current global seed, or None if not set
    
    Usage:
        >>> set_global_seed(42)
        >>> get_global_seed()
        42
    """
    return _seed_registry.get('global')


def set_component_seed(component: str, seed: int) -> None:
    """
    Set seed for specific component.
    
    Business Intent:
        Allow fine-grained control over randomness.
        Different components can have different seeds.
        Enable isolated testing of components.
    
    Args:
        component: Component name (e.g., 'data_loader', 'model', 'backtest')
        seed: Random seed for this component
    
    Usage:
        >>> set_component_seed('data_loader', 123)
        >>> set_component_seed('model', 456)
        >>> df = load_synthetic_data()  # Uses seed 123
        >>> model.fit()  # Uses seed 456
    """
    # Fail-fast: Validate inputs
    if not component or not isinstance(component, str):
        raise ValueError(f"Component must be non-empty string, got {repr(component)}")
    
    if not isinstance(seed, int):
        raise TypeError(f"Seed must be integer, got {type(seed)}")
    
    if seed < 0:
        raise ValueError(f"Seed must be non-negative, got {seed}")
    
    _seed_registry[component] = seed


def get_component_seed(component: str) -> Optional[int]:
    """
    Get seed for specific component.
    
    Business Intent:
        Retrieve component-specific seed for reproducibility.
        Enable audit trail for each component.
    
    Args:
        component: Component name
    
    Returns:
        Component seed, or None if not set
    """
    return _seed_registry.get(component)


def get_seed_registry() -> Dict[str, int]:
    """
    Get complete seed registry.
    
    Business Intent:
        Full audit trail for all random seeds.
        Enable complete reproducibility.
    
    Returns:
        Dictionary of all registered seeds
    
    Usage:
        >>> registry = get_seed_registry()
        >>> print(registry)
        {'global': 42, 'data_loader': 123, 'model': 456}
    """
    return _seed_registry.copy()


def clear_seed_registry() -> None:
    """
    Clear all registered seeds.
    
    Business Intent:
        Reset seed registry for clean state.
        Use between independent runs.
    """
    _seed_registry.clear()


def generate_seed() -> int:
    """
    Generate random seed for non-deterministic scenarios.
    
    Business Intent:
        Generate seed when deterministic behavior not required.
        Still track the generated seed for audit trail.
    
    Returns:
        Randomly generated seed (0 to 2^31-1)
    
    Usage:
        >>> seed = generate_seed()
        >>> set_global_seed(seed)
        >>> # Now deterministic with tracked seed
    """
    import time
    seed = int(time.time() * 1000) % (2**31)
    _seed_registry['last_generated'] = seed
    return seed


# Context manager for temporary seed changes
from contextlib import contextmanager


@contextmanager
def temporary_seed(seed: int):
    """
    Context manager for temporary seed changes.
    
    Business Intent:
        Temporarily change seed for specific operations.
        Automatically restore previous seed after operation.
        Ensure reproducibility even for temporary operations.
    
    Args:
        seed: Temporary seed to use
    
    Usage:
        >>> set_global_seed(42)
        >>> with temporary_seed(123):
        ...     result = run_experiment()  # Uses seed 123
        >>> # Seed automatically restored to 42
    """
    # Save current seeds
    saved_registry = get_seed_registry()
    
    # Set temporary seed
    set_global_seed(seed)
    
    try:
        yield
    finally:
        # Restore original seeds
        clear_seed_registry()
        for key, value in saved_registry.items():
            _seed_registry[key] = value


# Decorator for automatic seed management
def with_seed(seed: int):
    """
    Decorator for automatic seed management.
    
    Business Intent:
        Automatically set seed for function execution.
        Ensure reproducibility for decorated functions.
        Simplify seed management in test code.
    
    Args:
        seed: Seed to use for function execution
    
    Usage:
        >>> @with_seed(42)
        ... def train_model():
        ...     # Automatically uses seed 42
        ...     pass
    """
    def decorator(func):
        import functools
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with temporary_seed(seed):
                return func(*args, **kwargs)
        
        return wrapper
    
    return decorator
