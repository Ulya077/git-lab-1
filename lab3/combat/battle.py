from typing import List
from .models import Combatant, Side, EventType, BattleEvent, Participant, BattleReport, Outcome

class Battle:
    def __init__(self, hero: Combatant, enemy: Combatant):
        self.hero, self.enemy, self.events, self.round = hero, enemy, [], 0
    def run(self) -> BattleReport:
        while self.hero.is_alive() and self.enemy.is_alive():
            self.round += 1
            self._strike(self.hero, Side.HERO, self.enemy, Side.ENEMY)
            if self.enemy.is_alive(): self._strike(self.enemy, Side.ENEMY, self.hero, Side.HERO)
        outcome = Outcome.VICTORY if self.hero.is_alive() else Outcome.DEFEAT
        return BattleReport(Participant.of(self.hero), Participant.of(self.enemy), outcome, list(self.events))
    def _strike(self, attacker, source, defender, target):
        hit = attacker.roll_damage()
        dealt = defender.receive_hit(hit.damage)
        etype = EventType.CRITICAL_HIT if hit.critical else EventType.HIT
        self._emit(BattleEvent(self.round, etype, source, target, dealt, defender.get_health()))
        if not defender.is_alive(): self._emit(BattleEvent(self.round, EventType.DEATH, source, target, 0, 0))
    def _emit(self, event: BattleEvent): self.events.append(event)