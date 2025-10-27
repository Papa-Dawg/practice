
import random
from roll_mechanics import damage_roll


def weapon_damage(character):

    if character.weapon == 'bowstaff':
        damage = damage_roll(10, 2)
        return damage
    elif character.weapon == 'brass_knuckles':
        damage = damage_roll(6, 4)
        return damage
    elif character.weapon == 'bow_and_arrow':
        damage = damage_roll(20, 1)
        return damage
    elif character.weapon == 'rapier':
        damage = damage_roll(12, 2)
        return damage
    elif character.weapon == 'surroundings':
        damage = damage_roll(12, random.randit())
        return damage
    elif character.weapon == 'pistol':
        damage = damage_roll(40, 1)
        return damage
