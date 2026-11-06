import random
from typing import List, TypeVar

T = TypeVar('T')

class Dice:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Dice, cls).__new__(cls)
            cls._instance.random = random.Random()
        return cls._instance
    def reseed(self, seed: int): self.random.seed(seed)
    def next_seed(self) -> int: return self.random.randint(0, 999999)
    def roll(self, min_val: int, max_val: int) -> int: return self.random.randint(min_val, max_val)
    def chance(self, probability: float) -> bool: return self.random.random() < probability
    def pick(self, options: List[T]) -> T: return self.random.choice(options)