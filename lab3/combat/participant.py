from dataclasses import dataclass

@dataclass(frozen=True)
class Participant:
    code: str
    name: str
    max_health: int

    @classmethod
    def of(cls, combatant):
        return cls(combatant.code, combatant.name, combatant.max_health)