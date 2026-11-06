from enum import Enum
from ..core.exceptions import UnknownCodeException
from ..item.catalog import ItemCatalog
from ..kit.factory import StarterKitFactory, WarriorKitFactory, RangerKitFactory, MageKitFactory

class HeroClass(Enum):
    WARRIOR = ("warrior", "Воин", 120, WarriorKitFactory)
    RANGER = ("ranger", "Следопыт", 100, RangerKitFactory)
    MAGE = ("mage", "Маг", 85, MageKitFactory)
    def __init__(self, code: str, display_name: str, base_health: int, factory_class: type):
        self._code, self._display_name, self._base_health, self._factory_class = code, display_name, base_health, factory_class
    def get_starter_kit(self, catalog: ItemCatalog) -> StarterKitFactory: return self._factory_class(catalog)
    @classmethod
    def by_code(cls, code: str) -> 'HeroClass':
        for hero_class in cls:
            if hero_class._code == code: return hero_class
        raise UnknownCodeException("Класс героя", code)
    @property
    def code(self) -> str: return self._code
    @property
    def display_name(self) -> str: return self._display_name
    @property
    def base_health(self) -> int: return self._base_health