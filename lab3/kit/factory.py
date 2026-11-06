from abc import ABC, abstractmethod
from ..item.item import Weapon, Armor
from ..item.catalog import ItemCatalog, DefaultCatalog

class StarterKitFactory(ABC):
    @abstractmethod
    def create_weapon(self) -> Weapon: pass
    @abstractmethod
    def create_armor(self) -> Armor: pass

class WarriorKitFactory(StarterKitFactory):
    def __init__(self, catalog: ItemCatalog): self._catalog = catalog
    def create_weapon(self) -> Weapon: return self._catalog.create_weapon(DefaultCatalog.TRAINING_SWORD)
    def create_armor(self) -> Armor: return self._catalog.create_armor(DefaultCatalog.CHAINMAIL)

class RangerKitFactory(StarterKitFactory):
    def __init__(self, catalog: ItemCatalog): self._catalog = catalog
    def create_weapon(self) -> Weapon: return self._catalog.create_weapon(DefaultCatalog.HUNTING_BOW)
    def create_armor(self) -> Armor: return self._catalog.create_armor(DefaultCatalog.LEATHER_ARMOR)

class MageKitFactory(StarterKitFactory):
    def __init__(self, catalog: ItemCatalog): self._catalog = catalog
    def create_weapon(self) -> Weapon: return self._catalog.create_weapon(DefaultCatalog.APPRENTICE_STAFF)
    def create_armor(self) -> Armor: return self._catalog.create_armor(DefaultCatalog.LINEN_ROBE)