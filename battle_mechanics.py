## This file handles the battle mechanics.

#Allows me to create different colored text output.
from colorama import Fore, Style, init

#Imports functions and classes from other files to use in the functions in this file.
from hero_classes import Acrobat, Fortunate, Brawler, Academic, Socialite, Elder
from enemy_classes import Orc
from roll_mechanics import dice_roll, weapon_damage
from modifiers import roll_add, damage_modifier
from data_save import save_character_health, save_character

init(autoreset=True)

def attack_choice():
    pass


def attack(character, enemy, difficulty): #Initiates a battle to the death between the character and the enemy. Difficulty determined by enemy stat.

    print(Fore.RED + f"!!! " + Fore.GREEN + f"{character.name}" + Fore.RESET + " has encountered " + Fore.RED + f"{enemy.name} the {enemy.species} !!!")

    roll_bonus = roll_add(character.luck) #Uses the roll function, and adds a small amount to the roll based on the character's luck.
    damage_bonus = damage_modifier(character.phys) #Uses the damage modifier function, which creates a multiplier based on the character's phys stat.

    while enemy.health > 0 and character.health > 0: #A while loop, which runs the code until one person's health hits 0 or below.

        enemy_damage = 0 #Initiates the enemy damage value, so that it can be added onto later.
        
        roll_result = dice_roll(20, 1)[0] #Gives the value of a d20 roll, used to see if the attack is successful or not.
        
        critical = (roll_result == 20) #A natural roll of 20 makes a hit critical.
        attack_attempt = roll_result + roll_bonus #Total roll value including the roll bonus.

        if attack_attempt >= difficulty and not critical: #The following code is what happens if the attack is successful, but not a critical hit.
            attack_roll = weapon_damage(character) #Uses the weapon damage function, giving the amount of base damage the character rolled.
            damage = attack_roll * damage_bonus #Takes the base damage and multiplies it by the damage bonus.
            enemy.health -= damage #The enemy health is decreased after every damage done to it.
            print(Fore.GREEN + f"{character.name}'s attack hits {enemy.name} with their {character.weapon} for {damage} damage!")
            if enemy.health <= 0:
                print(Fore.MAGENTA + Style.BRIGHT + f"{character.name} has slain {enemy.name} with {damage} damage!")
                break #Ends the fight when the enemy health hits 0.
            else:
                print(f"{enemy.name} has {enemy.health} health remaining.")
        elif attack_attempt >= difficulty and critical: #Similar to above, but includes a "*2" multiplier when the hit is critical.
            attack_roll = weapon_damage(character)
            damage = attack_roll * damage_bonus * 2
            enemy.health -= damage
            print(Fore.GREEN + Style.BRIGHT + f"{character.name}'s attack critically hits {enemy.name} with their {character.weapon} for {damage} damage!")
            if enemy.health <= 0:
                print(Fore.MAGENTA + Style.BRIGHT + f"{character.name} has obliterated {enemy.name} with {damage} damage!")
                break
            else:
                print(f"{enemy.name} has {enemy.health} health remaining.")
        else: #What happens if neither of the above conditions happen, AKA, when the attack does NOT hit.
            enemy_attack = dice_roll(die = 8, number = 2) #Enemy damage roll, will be moved to another function later so that it's not always the same.
            for roll in enemy_attack:
                enemy_damage += int(roll) #enemy_damage is increased from 0 by whatever rolled.
            character.health -= enemy_damage #character health is decreased by enemy damage.
            print(Fore.RED + f"{character.name}'s attack fails to hit!")
            print(Fore.YELLOW + f"{enemy.name} hits {character.name} for {enemy_damage} damage!")
            if character.health <= 0:
                print(Fore.RED + Style.BRIGHT + f"{character.name} has been slain by {enemy.name}!")
                break
            else:
                print(Fore.CYAN + f"{character.name} has {character.health} health remaining!")
    
    if enemy.health > 0: #What happens after the battle is over, and the hero died (enemy not dead).
        print("\n*** The battle is over, and " + Fore.RED + Style.BRIGHT + f"{enemy.name}" + Fore.RESET + " has emerged victorious! ***")
        save_character_health(character)
        save_character(character)
        return character.health
    
    if character.health > 0: #What happens after the battle is over, and the enemy died (character not dead).
        print("\n*** The battle is over, and " + Fore.GREEN + Style.BRIGHT + f"{character.name}" + Fore.RESET + " has emerged victorious! ***")
        save_character_health(character)
        save_character(character)
        return character.health
    

my_acrobat = Acrobat(name = 'Nathan', age = 33, sex = 'male', height = 180)

my_brawler = Brawler(name = 'Joseph', age = 35, sex = 'male', height = 183)

my_academic = Academic(name = 'Samuel', age = 37, sex = 'male', height = 180)

my_socialite = Socialite(name = 'Jeromy', age = 31, sex = 'male', height = 178)

my_elder = Elder(name = 'Coles', age = 31, sex = 'male', height = 178)

my_fortunate = Fortunate(name = 'Zach', age = 33, sex = 'male', height = 178)

enemy = Orc(name = 'Bork')

attack(my_fortunate, enemy, 15)
