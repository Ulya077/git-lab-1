from typing import List
from ..core.exceptions import UnknownCodeException
from ..hero.hero import Hero
from ..item.item import Item
from ..item.catalog import ItemCatalog

class Merchant:
    def __init__(self, catalog: ItemCatalog, assortment: List[str]): self._catalog, self._assortment = catalog, list(assortment)
    def get_showcase(self) -> List[Item]: return [self._catalog.create(code) for code in self._assortment]
    def buy(self, hero: Hero, code: str) -> Item:
        if code not in self._assortment: raise UnknownCodeException("Товар", code)
        item = self._catalog.create(code)
        hero.spend_gold(item.get_price())
        hero.add_item(item)
        return item
    def sell(self, hero: Hero, item: Item) -> int:
        price = item.get_price() // 2
        hero.remove_item(item)
        hero.add_gold(price)
        return price