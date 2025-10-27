
from colorama import Fore, Style, init

from hero_classes import Acrobat
from enemy_classes import Orc
from roll_mechanics import dice_roll, weapon_damage
from modifiers import roll_add, damage_modifier
from data_save import save_character_health, save_character

init(autoreset=True)

def attack(character, enemy, difficulty):

    roll_bonus = roll_add(character.luck)
    damage_bonus = damage_modifier(character.phys)

    while enemy.health > 0 and character.health > 0:

        enemy_damage = 0
        
        roll_result = dice_roll(20, 1)[0]
        
        critical = (roll_result == 20)
        attack_attempt = roll_result + roll_bonus

        if attack_attempt >= difficulty and not critical:
            attack_roll = weapon_damage(character)
            damage = attack_roll * damage_bonus
            enemy.health -= damage
            print(Fore.GREEN + f"{character.name}'s attack hits {enemy.name} with their {character.weapon} for {damage} damage!")
            if enemy.health <= 0:
                print(Fore.MAGENTA + Style.BRIGHT + f"{character.name} has slain {enemy.name} with {damage} damage!")
                break
            else:
                print(f"{enemy.name} has {enemy.health} health remaining.")
        elif attack_attempt >= difficulty and critical:
            attack_roll = weapon_damage(character)
            damage = attack_roll * damage_bonus * 2
            enemy.health -= damage
            print(Fore.GREEN + Style.BRIGHT + f"{character.name}'s attack critically hits {enemy.name} with their {character.weapon} for {damage} damage!")
            if enemy.health <= 0:
                print(Fore.MAGENTA + Style.BRIGHT + f"{character.name} has obliterated {enemy.name} with {damage} damage!")
                break
            else:
                print(f"{enemy.name} has {enemy.health} health remaining.")
        else:
            enemy_attack = dice_roll(die = 8, number = 2)
            for roll in enemy_attack:
                enemy_damage += int(roll)
            character.health -= enemy_damage
            print(Fore.RED + f"{character.name}'s attack fails to hit!")
            print(Fore.YELLOW + f"{enemy.name} hits {character.name} for {enemy_damage} damage!")
            if character.health <= 0:
                print(Fore.RED + Style.BRIGHT + f"{character.name} has been slain by {enemy.name}!")
                break
            else:
                print(Fore.CYAN + f"{character.name} has {character.health} health remaining!")
    
    if enemy.health > 0:
        print("\n*** The battle is over, and " + Fore.RED + Style.BRIGHT + f"{enemy.name}" + Fore.RESET + " has emerged victorious! ***")
        save_character_health(character)
        save_character(character)
        return character.health
    
    if character.health > 0:
        print("\n*** The battle is over, and " + Fore.GREEN + Style.BRIGHT + f"{character.name}" + Fore.RESET + " has emerged victorious! ***")
        save_character_health(character)
        save_character(character)
        return character.health
    

my_acrobat = Acrobat(name = 'Nathan', age = 33, sex = 'male', height = 180)

enemy = Orc

attack(my_acrobat, enemy, 15)
