from lab3.core.dice import Dice
from lab3.hero.hero import HeroBuilder
from lab3.hero.hero_class import HeroClass
from lab3.item.catalog import DefaultCatalog
from lab3.item.models import Enchantment, FIERY
from lab3.world.location import Forest, Crypt
from lab3.view.console_view import ConsoleView

def main():
    catalog = DefaultCatalog.create()
    view = ConsoleView()
    print("===== Одиночка =====")
    first = Dice()
    second = Dice()
    print(f"Dice() возвращает один и тот же объект: {first is second}\n")
    print("===== Прототип =====")
    plain_sword = catalog.create(DefaultCatalog.IRON_SWORD)
    fiery_sword = catalog.create(DefaultCatalog.IRON_SWORD)
    fiery_sword.enchant(FIERY)
    print(f"Первая копия:        {view.describe(plain_sword)}")
    print(f"Вторая копия:        {view.describe(fiery_sword)}")
    print(f"Новая копия шаблона: {view.describe(catalog.create(DefaultCatalog.IRON_SWORD))}")
    print(f"Копии - разные объекты: {plain_sword is not fiery_sword}\n")
    print("===== Абстрактная фабрика =====")
    for hero_class in HeroClass:
        kit = hero_class.get_starter_kit(catalog)
        print(f"{hero_class.display_name}: {view.describe(kit.create_weapon())}, {view.describe(kit.create_armor())}")
    print()
    print("===== Строитель =====")
    hero = (HeroBuilder().set_name("Артур").set_hero_class(HeroClass.WARRIOR).set_starter_kit(HeroClass.WARRIOR.get_starter_kit(catalog)).set_level(3).build())
    view.print_hero(hero)
    try: (HeroBuilder().set_hero_class(HeroClass.MAGE).set_starter_kit(HeroClass.MAGE.get_starter_kit(catalog)).build())
    except ValueError as e: print(f"Герой без имени не создается: {e}")
    try: (HeroBuilder().set_name("Мерлин").build())
    except ValueError as e: print(f"Герой без класса не создается: {e}\n")
    print("===== Фабричный метод =====")
    forest = Forest(catalog)
    crypt = Crypt(catalog)
    view.print_report(forest.explore(hero, 7), forest.get_display_name())
    print()
    view.print_report(crypt.explore(hero, 7), crypt.get_display_name())

if __name__ == "__main__":
    main()