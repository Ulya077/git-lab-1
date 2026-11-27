from unittest.mock import create_autospec, patch
from lab3.core.dice import Dice
from lab3.defense.damage import Damage
from lab3.defense.damage_handler import DamageHandler
from lab3.defense.evasion_handler import EvasionHandler

def test_evades_and_stops_chain():
    dice_mock = create_autospec(Dice, instance=True)
    dice_mock.chance.return_value = True
    next_handler = create_autospec(DamageHandler, instance=True)
    
    handler = EvasionHandler(0.3)
    handler.set_next(next_handler)
    damage = Damage(40)

    with patch("lab3.defense.evasion_handler.Dice", return_value=dice_mock):
        handler.handle(damage)

    assert damage.amount == 0
    assert damage.evaded is True
    assert next_handler.mock_calls == []