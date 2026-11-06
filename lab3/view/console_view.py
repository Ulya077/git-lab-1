from ..combat.models import BattleEvent, BattleReport, Outcome, Side
from ..hero.hero import Hero
from ..item.item import Item
from ..world.models import ExpeditionReport, Rewards

class ConsoleView:
    def describe(self, item: Item) -> str:
        desc = item.get_name()
        enchants = item.get_enchantments()
        if enchants: desc += f" [{', '.join(e.name for e in enchants)}]"
        return f"{desc} ({item.get_description()})"
    def print_hero(self, hero: Hero):
        print(f"{hero.get_name()}, {hero.get_hero_class().display_name} {hero.get_level()} ур. | здоровье {hero.get_max_health()} | опыт {hero.get_experience()}/{hero.get_experience_to_next_level()} | золото {hero.get_gold()}")
        print(f"  Оружие: {self.describe(hero.get_weapon())}")
        print(f"  Броня:  {self.describe(hero.get_armor())}")
    def print_report(self, report: ExpeditionReport, location_name: str):
        battle = report.battle
        print(f"=== {location_name} (сид {report.seed}) ===")
        print(f"{battle.hero.name} встречает врага: {battle.enemy.name} ({battle.enemy.max_health} здоровья)")
        for event in battle.events:
            source = battle.hero if event.source == Side.HERO else battle.enemy
            target = battle.hero if event.target == Side.HERO else battle.enemy
            if event.type.value == "HIT":
                print(f"[раунд {event.round}] {source.name} -> {target.name}: {event.amount} урона, осталось {event.target_health_after}/{target.max_health}")
            elif event.type.value == "CRITICAL_HIT":
                print(f"[раунд {event.round}] {source.name} -> {target.name}: КРИТ! {event.amount} урона, осталось {event.target_health_after}/{target.max_health}")
            elif event.type.value == "DEATH":
                print(f"{target.name} повержен!")
        if battle.outcome == Outcome.DEFEAT:
            print(f"Поражение... {battle.hero.name} едва уносит ноги и теряет {-report.rewards.gold} золота")
        else:
            print(f"Победа! +{report.rewards.experience} опыта, +{report.rewards.gold} золота")
            if report.rewards.loot: print(f"Добыча: {self.describe(report.rewards.loot)}")
            if report.rewards.levels_gained > 0: print("Новый уровень!")