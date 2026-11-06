from dataclasses import dataclass
from typing import Optional
from ..item.item import Item
from ..combat.models import BattleReport

@dataclass
class Rewards: experience: int; gold: int; loot: Optional[Item]; levels_gained: int

@dataclass
class ExpeditionReport: seed: int; location_code: str; battle: BattleReport; rewards: Rewards