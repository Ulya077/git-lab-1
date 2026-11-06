from dataclasses import dataclass
from typing import List
from enum import Enum
from abc import ABC, abstractmethod

class Side(Enum):
    HERO = "HERO"
    ENEMY = "ENEMY"

class EventType(Enum):
    HIT = "HIT"
    CRITICAL_HIT = "CRITICAL_HIT"
    DEATH = "DEATH"

class Outcome(Enum):
    VICTORY = "VICTORY"
    DEFEAT = "DEFEAT"

@dataclass(frozen=True)
class Hit:
    damage: int
    critical: bool

@dataclass
class BattleEvent:
    round: int
    type: EventType
    source: Side
    target: Side
    amount: int
    target_health_after: int

@dataclass(frozen=True)
class Participant:
    code: str
    name: str
    max_health: int

    @classmethod
    def of(cls, combatant):
        return cls(combatant.get_code(), combatant.get_name(), combatant.get_max_health())

@dataclass
class BattleReport:
    hero: Participant
    enemy: Participant
    outcome: Outcome
    events: List[BattleEvent]

class Combatant(ABC):
    @abstractmethod
    def get_code(self) -> str: pass
    @abstractmethod
    def get_name(self) -> str: pass
    @abstractmethod
    def get_health(self) -> int: pass
    @abstractmethod
    def get_max_health(self) -> int: pass
    @abstractmethod
    def is_alive(self) -> bool: pass
    @abstractmethod
    def roll_damage(self): pass
    @abstractmethod
    def receive_hit(self, damage: int) -> int: pass
