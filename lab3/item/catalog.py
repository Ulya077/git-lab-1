from typing import List, Dict
from ..core.exceptions import UnknownCodeException
from .item import Item, Weapon, Armor, Sword, Bow, Staff

class ItemCatalog:
    def __init__(self): self._prototypes: Dict[str, Item] = {}
    def register(self, prototype: Item): self._prototypes[prototype.get_code()] = prototype
    def create(self, code: str) -> Item:
        prototype = self._prototypes.get(code)
        if prototype is None: raise UnknownCodeException("Предмет", code)
        return prototype.copy()
    def create_weapon(self, code: str) -> Weapon:
        item = self.create(code)
        if isinstance(item, Weapon): return item
        raise ValueError(f"Предмет '{code}' не является оружием")
    def create_armor(self, code: str) -> Armor:
        item = self.create(code)
        if isinstance(item, Armor): return item
        raise ValueError(f"Предмет '{code}' не является броней")

class DefaultCatalog:
    TRAINING_SWORD, HUNTING_BOW, APPRENTICE_STAFF = "training-sword", "hunting-bow", "apprentice-staff"
    CHAINMAIL, LEATHER_ARMOR, LINEN_ROBE = "chainmail", "leather-armor", "linen-robe"
    IRON_SWORD, ELVEN_BOW, EMBER_STAFF, PLATE_ARMOR = "iron-sword", "elven-bow", "ember-staff", "plate-armor"
    GOBLIN_CLEAVER, BONE_BOW, NECROMANCER_STAFF = "goblin-cleaver", "bone-bow", "necromancer-staff"
    KNIGHT_BLADE, CRYPT_MAIL, DAWN_BLADE, DRAGONSCALE_ARMOR = "knight-blade", "crypt-mail", "dawn-blade", "dragonscale-armor"
    @staticmethod
    def create() -> ItemCatalog:
        c = ItemCatalog()
        c.register(Sword(DefaultCatalog.TRAINING_SWORD, "Тренировочный меч", 20, 12))
        c.register(Bow(DefaultCatalog.HUNTING_BOW, "Охотничий лук", 20, 10, 0.3))
        c.register(Staff(DefaultCatalog.APPRENTICE_STAFF, "Посох ученика", 20, 14, 0.3))
        c.register(Armor(DefaultCatalog.CHAINMAIL, "Кольчуга", 40, 0.3))
        c.register(Armor(DefaultCatalog.LEATHER_ARMOR, "Кожаная броня", 30, 0.2))
        c.register(Armor(DefaultCatalog.LINEN_ROBE, "Льняная роба", 15, 0.1))
        c.register(Sword(DefaultCatalog.IRON_SWORD, "Железный меч", 80, 17))
        c.register(Bow(DefaultCatalog.ELVEN_BOW, "Эльфийский лук", 90, 14, 0.4))
        c.register(Staff(DefaultCatalog.EMBER_STAFF, "Тлеющий посох", 90, 20, 0.3))
        c.register(Armor(DefaultCatalog.PLATE_ARMOR, "Латы", 120, 0.4))
        c.register(Sword(DefaultCatalog.GOBLIN_CLEAVER, "Гоблинский тесак", 40, 15))
        c.register(Bow(DefaultCatalog.BONE_BOW, "Костяной лук", 140, 17, 0.4))
        c.register(Staff(DefaultCatalog.NECROMANCER_STAFF, "Посох некроманта", 150, 25, 0.35))
        c.register(Sword(DefaultCatalog.KNIGHT_BLADE, "Клинок рыцаря", 150, 23))
        c.register(Armor(DefaultCatalog.CRYPT_MAIL, "Кольчуга стража склепа", 160, 0.45))
        c.register(Sword(DefaultCatalog.DAWN_BLADE, "Клинок рассвета", 500, 35))
        c.register(Armor(DefaultCatalog.DRAGONSCALE_ARMOR, "Драконья чешуя", 500, 0.55))
        return c