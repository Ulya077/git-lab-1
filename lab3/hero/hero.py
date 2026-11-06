from typing import List
from ..combat.models import Combatant, Hit
from ..item.item import Item, Weapon, Armor
from ..kit.factory import StarterKitFactory
from .hero_class import HeroClass

class HeroBuilder:
    def __init__(self):
        self._name, self._hero_class, self._weapon, self._armor = None, None, None, None
        self._level, self._gold = 1, 50
    def set_name(self, name: str) -> 'HeroBuilder': self._name = name; return self
    def set_hero_class(self, hero_class: HeroClass) -> 'HeroBuilder': self._hero_class = hero_class; return self
    def set_weapon(self, weapon: Weapon) -> 'HeroBuilder': self._weapon = weapon; return self
    def set_armor(self, armor: Armor) -> 'HeroBuilder': self._armor = armor; return self
    def set_starter_kit(self, starter_kit: StarterKitFactory) -> 'HeroBuilder':
        self._weapon = starter_kit.create_weapon(); self._armor = starter_kit.create_armor(); return self
    def set_level(self, level: int) -> 'HeroBuilder': self._level = level; return self
    def set_gold(self, gold: int) -> 'HeroBuilder': self._gold = gold; return self
    def build(self) -> 'Hero':
        if not self._name or not self._name.strip(): raise ValueError("У героя должно быть имя")
        if len(self._name) > 20: raise ValueError("Имя героя не может быть длиннее 20 символов")
        if self._hero_class is None: raise ValueError("Не выбран класс героя")
        if self._weapon is None or self._armor is None: raise ValueError("Герою нужны оружие и броня")
        if self._level < 1: raise ValueError("Уровень героя не может быть меньше 1")
        if self._gold < 0: raise ValueError("Золота не может быть меньше нуля")
        return Hero(self)

class Hero(Combatant):
    def __init__(self, builder: HeroBuilder):
        self._name, self._hero_class, self._level = builder._name, builder._hero_class, builder._level
        self._experience, self._gold = 0, builder._gold
        self._weapon, self._armor = builder._weapon, builder._armor
        self._inventory: List[Item] = []
        self._health = self.get_max_health()
    def roll_damage(self) -> Hit:
        hit = self._weapon.roll_damage()
        return Hit(hit.damage + (self._level - 1) * 3, hit.critical)
    def receive_hit(self, damage: int) -> int:
        dealt = max(1, int(round(damage * (1 - self._armor.get_defense()))))
        self._health = max(0, self._health - dealt)
        return dealt
    def is_alive(self) -> bool: return self._health > 0
    def restore_health(self): self._health = self.get_max_health()
    def gain_experience(self, amount: int) -> int:
        self._experience += amount
        levels_gained = 0
        while self._experience >= self.get_experience_to_next_level():
            self._experience -= self.get_experience_to_next_level()
            self._level += 1; levels_gained += 1
        return levels_gained
    def add_gold(self, amount: int): self._gold += amount
    def spend_gold(self, amount: int):
        if amount > self._gold: raise ValueError(f"Не хватает золота: нужно {amount}, есть {self._gold}")
        self._gold -= amount
    def add_item(self, item: Item): self._inventory.append(item)
    def remove_item(self, item: Item):
        if item not in self._inventory: raise ValueError(f"В инвентаре нет предмета {item.get_name()}")
        self._inventory.remove(item)
    def equip(self, item: Item):
        if isinstance(item, Weapon): self.remove_item(item); self._inventory.append(self._weapon); self._weapon = item
        elif isinstance(item, Armor): self.remove_item(item); self._inventory.append(self._armor); self._armor = item
        else: raise ValueError(f"Предмет нельзя экипировать: {item.get_name()}")
    def get_code(self) -> str: return self._hero_class.code
    def get_name(self) -> str: return self._name
    def get_health(self) -> int: return self._health
    def get_max_health(self) -> int: return self._hero_class.base_health + (self._level - 1) * 15
    def get_hero_class(self) -> HeroClass: return self._hero_class
    def get_level(self) -> int: return self._level
    def get_experience(self) -> int: return self._experience
    def get_experience_to_next_level(self) -> int: return self._level * 100
    def get_gold(self) -> int: return self._gold
    def get_weapon(self) -> Weapon: return self._weapon
    def get_armor(self) -> Armor: return self._armor
    def get_inventory(self) -> List[Item]: return list(self._inventory)