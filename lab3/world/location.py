from abc import ABC, abstractmethod
from typing import List
from ..combat.battle import Battle
from ..combat.models import Outcome
from ..core.dice import Dice
from ..core.exceptions import UnknownCodeException
from ..enemy.enemy import Enemy
from ..hero.hero import Hero
from ..item.item import Item
from ..item.catalog import ItemCatalog, DefaultCatalog
from .models import Rewards, ExpeditionReport

class Location(ABC):
    def __init__(self, code: str, display_name: str, recommended_level: int, catalog: ItemCatalog):
        self._code, self._display_name, self._recommended_level, self._catalog = code, display_name, recommended_level, catalog
    @abstractmethod
    def _create_enemy(self) -> Enemy: pass
    @abstractmethod
    def _get_loot_table(self) -> List[str]: pass
    def explore(self, hero: Hero, seed: int = None) -> ExpeditionReport:
        dice = Dice()
        seed = seed if seed is not None else dice.next_seed()
        dice.reseed(seed)
        hero.restore_health()
        enemy = self._create_enemy()
        battle = Battle(hero, enemy).run()
        rewards = self._reward(hero, enemy, dice) if battle.outcome == Outcome.VICTORY else self._punish(hero)
        return ExpeditionReport(seed, self._code, battle, rewards)
    def _reward(self, hero: Hero, enemy: Enemy, dice: Dice) -> Rewards:
        loot = self._roll_loot(dice)
        levels = hero.gain_experience(enemy.get_experience_reward())
        hero.add_gold(enemy.roll_gold_reward())
        if loot: hero.add_item(loot)
        return Rewards(enemy.get_experience_reward(), enemy.roll_gold_reward(), loot, levels)
    def _roll_loot(self, dice: Dice) -> Item:
        if not dice.chance(0.6): return None
        loot = self._catalog.create(dice.pick(self._get_loot_table()))
        if dice.chance(0.3): loot.enchant(dice.pick(loot.get_possible_enchantments()))
        return loot
    def _punish(self, hero: Hero) -> Rewards:
        lost = hero.get_gold() // 2
        hero.spend_gold(lost)
        return Rewards(0, -lost, None, 0)
    def get_code(self) -> str: return self._code
    def get_display_name(self) -> str: return self._display_name
    def get_recommended_level(self) -> int: return self._recommended_level

class Forest(Location):
    def __init__(self, catalog: ItemCatalog): super().__init__("forest", "Мистический лес", 1, catalog)
    def _create_enemy(self) -> Enemy:
        from ..enemy.enemy import Goblin
        return Goblin()
    def _get_loot_table(self) -> List[str]: return [DefaultCatalog.GOBLIN_CLEAVER, DefaultCatalog.HUNTING_BOW, DefaultCatalog.LEATHER_ARMOR]

class Crypt(Location):
    def __init__(self, catalog: ItemCatalog): super().__init__("crypt", "Заброшенный склеп", 3, catalog)
    def _create_enemy(self) -> Enemy:
        from ..enemy.enemy import Skeleton
        return Skeleton()
    def _get_loot_table(self) -> List[str]: return [DefaultCatalog.KNIGHT_BLADE, DefaultCatalog.BONE_BOW, DefaultCatalog.NECROMANCER_STAFF, DefaultCatalog.CRYPT_MAIL]

class DragonLair(Location):
    def __init__(self, catalog: ItemCatalog): super().__init__("dragon-lair", "Логово дракона", 5, catalog)
    def _create_enemy(self) -> Enemy:
        from ..enemy.enemy import Dragon
        return Dragon()
    def _get_loot_table(self) -> List[str]: return [DefaultCatalog.DAWN_BLADE, DefaultCatalog.DRAGONSCALE_ARMOR]

class LocationRegistry:
    def __init__(self, locations: List[Location]): self._locations = {loc.get_code(): loc for loc in locations}
    def get(self, code: str) -> Location:
        if code not in self._locations: raise UnknownCodeException("Локация", code)
        return self._locations[code]
    def get_all(self) -> List[Location]: return list(self._locations.values())