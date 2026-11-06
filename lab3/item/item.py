from abc import ABC, abstractmethod
from typing import List
from ..combat.models import Hit
from .models import Enchantment, FOR_WEAPONS, FOR_ARMOR

class Item(ABC):
    def __init__(self, code: str, name: str, base_price: int):
        self._code, self._name, self._base_price, self._enchantments = code, name, base_price, []
    def _init_copy(self, source: 'Item'):
        self._code, self._name, self._base_price = source._code, source._name, source._base_price
        self._enchantments = list(source._enchantments)
    @abstractmethod
    def copy(self) -> 'Item': pass
    @abstractmethod
    def get_possible_enchantments(self) -> List[Enchantment]: pass
    @abstractmethod
    def get_description(self) -> str: pass
    def enchant(self, enchantment: Enchantment):
        if enchantment not in self.get_possible_enchantments(): raise ValueError(f"Зачарование '{enchantment.name}' не подходит")
        self._enchantments.append(enchantment)
    def get_code(self) -> str: return self._code
    def get_name(self) -> str: return self._name
    def get_price(self) -> int: return self._base_price + sum(e.bonus_price for e in self._enchantments)
    def get_enchantments(self) -> List[Enchantment]: return list(self._enchantments)

class Weapon(Item, ABC):
    def __init__(self, code: str, name: str, base_price: int, damage: int):
        super().__init__(code, name, base_price); self._damage = damage
    def _init_copy(self, source: 'Weapon'): super()._init_copy(source); self._damage = source._damage
    @abstractmethod
    def roll_damage(self) -> Hit: pass
    @abstractmethod
    def copy(self) -> 'Weapon': pass
    def get_damage(self) -> int: return self._damage + sum(e.bonus_damage for e in self.get_enchantments())
    def get_possible_enchantments(self) -> List[Enchantment]: return FOR_WEAPONS

class Sword(Weapon):
    def __init__(self, code: str, name: str, base_price: int, damage: int): super().__init__(code, name, base_price, damage)
    def _init_copy(self, source: 'Sword'): super()._init_copy(source)
    def roll_damage(self) -> Hit: return Hit(self.get_damage(), False)
    def copy(self) -> 'Sword':
        new_obj = Sword.__new__(Sword); new_obj._init_copy(self); return new_obj
    def get_description(self) -> str: return f"урон {self.get_damage()}"

class Bow(Weapon):
    def __init__(self, code: str, name: str, base_price: int, damage: int, critical_chance: float): super().__init__(code, name, base_price, damage); self._critical_chance = critical_chance
    def _init_copy(self, source: 'Bow'): super()._init_copy(source); self._critical_chance = source._critical_chance
    def roll_damage(self) -> Hit:
        from ..core.dice import Dice
        return Hit(self.get_damage() * 2, True) if Dice().chance(self._critical_chance) else Hit(self.get_damage(), False)
    def copy(self) -> 'Bow':
        new_obj = Bow.__new__(Bow); new_obj._init_copy(self); return new_obj
    def get_description(self) -> str: return f"урон {self.get_damage()}, шанс крита {int(self._critical_chance * 100)}%"

class Staff(Weapon):
    def __init__(self, code: str, name: str, base_price: int, damage: int, scatter: float): super().__init__(code, name, base_price, damage); self._scatter = scatter
    def _init_copy(self, source: 'Staff'): super()._init_copy(source); self._scatter = source._scatter
    def roll_damage(self) -> Hit:
        from ..core.dice import Dice
        return Hit(Dice().roll(self._get_min(), self._get_max()), False)
    def copy(self) -> 'Staff':
        new_obj = Staff.__new__(Staff); new_obj._init_copy(self); return new_obj
    def get_description(self) -> str: return f"урон {self._get_min()}-{self._get_max()}"
    def _get_min(self) -> int: return int(round(self.get_damage() * (1 - self._scatter)))
    def _get_max(self) -> int: return int(round(self.get_damage() * (1 + self._scatter)))

class Armor(Item):
    MAX_DEFENSE = 0.75
    def __init__(self, code: str, name: str, base_price: int, defense: float): super().__init__(code, name, base_price); self._defense = defense
    def _init_copy(self, source: 'Armor'): super()._init_copy(source); self._defense = source._defense
    def copy(self) -> 'Armor':
        new_obj = Armor.__new__(Armor); new_obj._init_copy(self); return new_obj
    def get_defense(self) -> float: return min(self._defense + sum(e.bonus_defense for e in self.get_enchantments()), self.MAX_DEFENSE)
    def get_possible_enchantments(self) -> List[Enchantment]: return FOR_ARMOR
    def get_description(self) -> str: return f"защита {int(round(self.get_defense() * 100))}%"