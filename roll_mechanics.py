
import random
from colorama import Fore, Style, init # type: ignore

from modifiers import roll_add, insight_add
from hero_classes import Acrobat
from enemy_classes import Orc

init(autoreset=True)

def dice_roll(die, number):

    rolls = []

    for roll in range(number):
        roll = random.randint(1, die)
        rolls.append(roll)
    
    return rolls


def damage_roll(die, num):
    damage = 0
    damage_roll = dice_roll(die, num)
    for roll in damage_roll:
        damage += roll
    
    return damage


def insight_check(character, difficulty):

    rolls = dice_roll(die = 20, number = 1)
    for roll in rolls:
        roll = int(roll)
    roll_bonus = roll_add(character.luck)
    insight_bonus = insight_add(character.inte)
    total = roll + roll_bonus + insight_bonus

    if total >= difficulty:
        print(f"*** {character.name} succeeds! ***")
        return True
    else:
        print(f"*** {character.name} fails! ***")
        return False
    

def weapon_damage(character):

    if character.weapon == 'bowstaff':
        damage = damage_roll(10, 2)
        return damage
    elif character.weapon == 'brass knuckles':
        damage = damage_roll(6, 4)
        return damage
    elif character.weapon == 'bow and arrow':
        damage = damage_roll(20, 1)
        return damage
    elif character.weapon == 'rapier':
        damage = damage_roll(12, 2)
        return damage
    elif character.weapon == 'surroundings':
        luck = random.randint(1, 4)
        damage = damage_roll(12, luck)
        return damage
    elif character.weapon == 'pistol':
        damage = damage_roll(40, 1)
        return damage
    

