# tests/test_grid_calculator.py

import pytest
from src.grid_calculator import GridCalculator

def test_calculate_static_grids():
    calculator = GridCalculator(lower_price=100, upper_price=200, grid_quantity=10, total_investment=1000)
    grids = calculator.calculate_static_grids()
    assert len(grids['prices']) == 11  # grid_quantity + 1
    assert len(grids['quantities']) == 11
    assert grids['prices'][0] == 100
    assert grids['prices'][-1] == 200
    assert all(q > 0 for q in grids['quantities'])

def test_calculate_dynamic_grids():
    calculator = GridCalculator(lower_price=100, upper_price=200, grid_quantity=10, total_investment=1000)
    grids = calculator.calculate_dynamic_grids(current_price=150, volatility=10, price_precision=2)
    assert len(grids['prices']) > 0
    assert len(grids['quantities']) > 0
    assert all(isinstance(price, float) for price in grids['prices'])
    assert all(q > 0 for q in grids['quantities'])

def test_dynamic_grids_out_of_range():
    calculator = GridCalculator(lower_price=100, upper_price=200, grid_quantity=10, total_investment=1000)
    with pytest.raises(ValueError):
        calculator.calculate_dynamic_grids(current_price=250, volatility=10, price_precision=2)