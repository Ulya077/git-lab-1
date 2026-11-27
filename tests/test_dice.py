import pytest
from lab3.core.dice import Dice

@pytest.fixture(autouse=True)
def reset_dice():
    Dice().reseed(2026)

def test_returns_same_instance():
    assert Dice() is Dice()

def test_rolls_stay_within_bounds():
    for _ in range(100):
        res = Dice().roll(1, 6)
        assert 1 <= res <= 6
