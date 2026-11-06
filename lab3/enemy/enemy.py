from abc import ABC, abstractmethod
from ..combat.models import Combatant, Hit
from ..core.dice import Dice

class Enemy(Combatant, ABC):
    @abstractmethod
    def get_experience_reward(self) -> int: pass
    @abstractmethod
    def roll_gold_reward(self) -> int: pass

class AbstractEnemy(Enemy):
    def __init__(self, code: str, name: str, max_health: int, min_damage: int, max_damage: int, exp_reward: int, gold_reward: int):
        self._code, self._name, self._max_health = code, name, max_health
        self._min_damage, self._max_damage = min_damage, max_damage
        self._exp_reward, self._gold_reward = exp_reward, gold_reward
        self._health = max_health
    def roll_damage(self) -> Hit: return Hit(Dice().roll(self._min_damage, self._max_damage), False)
    def receive_hit(self, damage: int) -> int:
        dealt = max(1, self._reduce_damage(damage))
        self._health = max(0, self._health - dealt)
        return dealt
    def _reduce_damage(self, damage: int) -> int: return damage
    def is_alive(self) -> bool: return self._health > 0
    def roll_gold_reward(self) -> int: return Dice().roll(self._gold_reward // 2, self._gold_reward)
    def get_experience_reward(self) -> int: return self._exp_reward
    def get_code(self) -> str: return self._code
    def get_name(self) -> str: return self._name
    def get_health(self) -> int: return self._health
    def get_max_health(self) -> int: return self._max_health

class Goblin(AbstractEnemy):
    def __init__(self): super().__init__("goblin", "Гоблин", 50, 6, 14, 40, 30)

class Skeleton(AbstractEnemy):
    def __init__(self): super().__init__("skeleton", "Скелет", 110, 10, 24, 90, 70)
    def _reduce_damage(self, damage: int) -> int: return int(round(damage * 0.7))

class Dragon(AbstractEnemy):
    def __init__(self): super().__init__("dragon", "Дракон", 260, 16, 22, 500, 400)
    def roll_damage(self) -> Hit:
        bite = super().roll_damage()
        return Hit(bite.damage * 2, True) if Dice().chance(0.25) else bite
    def _reduce_damage(self, damage: int) -> int: return int(round(damage * 0.75))