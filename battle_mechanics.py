## This file handles the battle mechanics.

import random

#Allows me to create different colored text output.
from colorama import Fore, Style, init

#Imports functions and classes from other files to use in the functions in this file.
from character_classes import Acrobat, Fortunate, Brawler, Academic, Socialite, Elder, Orc
from data_save import save_character

init(autoreset=True) #Resets the color I add after every printed line. It would color everything after, otherwise.


############################################################# Modifiers ###################################################################

def damage_modifier(phys):
    modifier = int(1 + (phys / 10)) #Makes the modifier 1.(whatever-phys-stat). So for the Acrobat, it would be 1.9. Which is prolly too high, idk.
    return modifier


def roll_add(luck): #Gives a bonus to rolls based on the character's luck, which is divided by 3, with the decimal part truncated.
    add = luck // 3
    return add


def insight_add(inte): #Insight bonus based on intelligence.
    add = inte
    return add

def social_add(soc): #Dialogue option bonus based on social stat.
    add = soc
    return add

def choice_add(wis): #Trynna think of how to make it work that the wisdom stat can benefit decision making.
    add = wis
    return add


############################################################# Basic Roll Logic ###################################################################


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
    

############################################################# Battle Mechanics ###################################################################
    

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


def attack_choice(character, enemy): #Gives choice between actions on what to do next.
    
    print(
        "\n======== Next? ========\n" +
        f"1) Use {character.weapon}\n" +
        "2) Use item\n" +
        f"3) Confuse {enemy.name}\n" +
        "4) Flee\n"
        )
    
    choice = '' #Sets the choice to an empty string, so that it won't be considered valid.
    valid_choices = ['1', '2', '3', '4'] #Sets what options are valid.
    while choice not in valid_choices: #Will keep asking until valid option is chosen.
        choice = input("Whatchu finna do? ").strip() #Because choice is currently '', it's not valid, so the user is asked to choose.
        if choice not in valid_choices: #If the user enters anything other than what's in valid_choices, they get the message below.
            print("Please enter a valid choice.")
    
    return choice #Returns the user's choice, which is used later on in the other function.
    

def regular_attack(character, enemy, damage_bonus): #Code for regular attack
    attack_roll = weapon_damage(character) #Uses the weapon damage function, giving the amount of base damage the character rolled.
    damage = attack_roll * damage_bonus #Takes the base damage and multiplies it by the damage bonus.
    enemy.health -= damage #The enemy health is decreased after every damage done to it.
    
    print(Fore.GREEN + f"{character.name}'s attack hits {enemy.name} with their {character.weapon} for {damage} damage!")
    
    return enemy.health, damage


def critical_attack(character, enemy, damage_bonus): #Code for critical hit
    attack_roll = weapon_damage(character)
    damage = attack_roll * damage_bonus * 2
    enemy.health -= damage
    
    print(Fore.GREEN + Style.BRIGHT + f"{character.name}'s attack critically hits {enemy.name} with their {character.weapon} for {damage} damage!")

    return enemy.health, damage


def confuse(character, enemy): #Code for confusion attempt
    base_chance_of_confuse = dice_roll(100, 1)[0]
    soc_bonus = social_add(character.soc)
    chance_of_confuse = base_chance_of_confuse + soc_bonus

    if chance_of_confuse >= enemy.mental:
        return True
    else:
        return False


def flee(character, enemy): #Code for flee attempt
    base_chance_of_flee = int(dice_roll(100, 1)[0])
    luck_bonus = int(roll_add(character.luck))
    chance_of_flee = base_chance_of_flee + luck_bonus
    if chance_of_flee >= enemy.flee:
        return True
    else:
        return False
    

def resolve_attack_attempt(character, enemy, roll_result, roll_bonus, damage_bonus, difficulty):
    """Processes a single attack roll (d20) and returns the game state updates."""

    attack_attempt = roll_result + roll_bonus
    critical = (roll_result == 20)
    
    # 1. PLAYER HITS (Regular or Critical)
    if attack_attempt >= difficulty:
        
        # Calculate damage (simplified for this example)
        base_damage = weapon_damage(character) 
        multiplier = 2 if critical else 1
        damage = base_damage * damage_bonus * multiplier
        
        # Apply damage
        enemy.health -= damage
        
        if critical:
            message = f"{character.name} critically hits {enemy.name} for {damage} damage!"
        else:
            message = f"{character.name}'s attack hits {enemy.name} for {damage} damage!"
            
        return "MONSTER_TURN", message # Returns the next phase and the message

    # 2. PLAYER MISSES (Enemy retaliates immediately)
    else:
        # Enemy's Counter Attack Logic (using your original enemy damage roll)
        enemy_damage_roll = dice_roll(die=8, number=2)
        enemy_damage = sum(enemy_damage_roll)
        
        character.health -= enemy_damage
        
        message = (
            f"{character.name}'s attack fails! | "
            f"{enemy.name} hits {character.name} for {enemy_damage} damage!"
        )
        
        return "PLAYER_TURN", message # Enemy retaliated, so it's the player's turn again


def attack(character, enemy, difficulty): #Initiates a battle to the death between the character and the enemy. Difficulty determined by enemy stat.

    print(Fore.RED + f"!!! " + Fore.GREEN + f"{character.name}" + Fore.RESET + " has encountered " + Fore.RED + f"{enemy.name} the {enemy.species} !!!")

    roll_bonus = roll_add(character.luck) #Uses the roll function, and adds a small amount to the roll based on the character's luck.
    damage_bonus = damage_modifier(character.phys) #Uses the damage modifier function, which creates a multiplier based on the character's phys stat.

    fled = False

    while enemy.health > 0 and character.health > 0: #A while loop, which runs the code until one person's health hits 0 or below.

        enemy_damage = 0 #Initiates the enemy damage value, so that it can be added onto later.
        
        roll_result = dice_roll(20, 1)[0] #Gives the value of a d20 roll, used to see if the attack is successful or not.
        
        critical = (roll_result == 20) #A natural roll of 20 makes a hit critical.
        attack_attempt = roll_result + roll_bonus #Total roll value including the roll bonus.

        choice = attack_choice(character, enemy)

        if choice == '1':
            if attack_attempt >= difficulty and not critical: #The following code is what happens if the attack is successful, but not a critical hit.
                enemy_health, damage = regular_attack(character, enemy, damage_bonus)
                if enemy_health <= 0:
                    print(Fore.MAGENTA + Style.BRIGHT + f"{character.name} has slain {enemy.name} with {damage} damage!")
                    break #Ends the fight when the enemy health hits 0.
                else:
                    print(Fore.RED + f"{enemy.name}" + Fore.RESET + " has " + Fore.YELLOW + f"{enemy.health}" + Fore.RESET + " health remaining.")
            elif attack_attempt >= difficulty and critical: #Similar to above, but includes a "*2" multiplier when the hit is critical.
                enemy_health, damage = critical_attack(character, enemy, damage_bonus)
                if enemy_health <= 0:
                    print(Fore.MAGENTA + Style.BRIGHT + f"{character.name} has obliterated {enemy.name} with {damage} damage!")
                    break
                else:
                    print(Fore.RED + f"{enemy.name}" + Fore.RESET + " has " + Fore.YELLOW + f"{enemy.health}" + Fore.RESET + " health remaining.")
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
        
        elif choice == '2': #Code for what happens if user chooses to use an item.
            pass
        elif choice == '3': #Code for what happens if user chooses to try to confuse the enemy.
            chance_of_confuse = confuse(character, enemy)
            if chance_of_confuse:
                print(Fore.RED + f"{enemy.name}" + Fore.GREEN + " has become confused!")
                if not critical: #If a critical wasn't rolled before the choice, the hero gets two regular attacks.
                    enemy_health, damage = regular_attack(character, enemy, damage_bonus)
                    if enemy_health <= 0:
                        print(Fore.MAGENTA + Style.BRIGHT + f"{character.name} has slain {enemy.name} with {damage} damage!")
                        break #Ends the fight when the enemy health hits 0.
                    else:
                        print(Fore.RED + f"{enemy.name}" + Fore.RESET + " has " + Fore.YELLOW + f"{enemy.health}" + Fore.RESET + " health remaining.")
                    print("Due to " + Fore.RED + f"{enemy.name}" + Fore.RESET + "'s confusion, " + Fore.GREEN + f"{character.name}" + Fore.RESET + " strikes again!")
                    enemy_health, damage = regular_attack(character, enemy, damage_bonus)
                    if enemy_health <= 0:
                        print(Fore.MAGENTA + Style.BRIGHT + f"{character.name} has slain {enemy.name} with {damage} damage!")
                        break #Ends the fight when the enemy health hits 0.
                    else:
                        print(Fore.RED + f"{enemy.name}" + Fore.RESET + " has " + Fore.YELLOW + f"{enemy.health}" + Fore.RESET + " health remaining.")
                else: #If a critical was rolled before the choice, the hero gets two critical attacks.
                    enemy_health, damage = critical_attack(character, enemy, damage_bonus)
                    if enemy_health <= 0:
                        print(Fore.MAGENTA + Style.BRIGHT + f"{character.name} has obliterated {enemy.name} with {damage} damage!")
                        break
                    else:
                        print(Fore.RED + f"{enemy.name}" + Fore.RESET + " has " + Fore.YELLOW + f"{enemy.health}" + Fore.RESET + " health remaining.")
                    print("Due to " + Fore.RED + f"{enemy.name}" + Fore.RESET + "'s confusion, " + Fore.GREEN + f"{character.name}" + Fore.RESET + " strikes again!")
                    enemy_health, damage = critical_attack(character, enemy, damage_bonus)
                    if enemy_health <= 0:
                        print(Fore.MAGENTA + Style.BRIGHT + f"{character.name} has obliterated {enemy.name} with {damage} damage!")
                        break
                    else:
                        print(Fore.RED + f"{enemy.name}" + Fore.RESET + " has " + Fore.YELLOW + f"{enemy.health}" + Fore.RESET + " health remaining.")
            else:
                print(Fore.GREEN + f"{character.name}" + Fore.RESET + "'s attempt to confuse the enemy has failed!")
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
        elif choice == '4': #Code for what happens if use tries to flee from the battle.
            chance_of_flee = flee(character, enemy)
            if chance_of_flee:
                fled = True
                break
            else:
                print(Fore.GREEN + f"{character.name}" + Fore.RED + "'s attempt at escape has failed!")
                fled = False


    if enemy.health > 0 and not fled: #What happens after the battle is over, and the hero died (enemy not dead).
        print("\n*** The battle is over, and " + Fore.RED + Style.BRIGHT + f"{enemy.name}" + Fore.RESET + " has emerged victorious! ***\n")
        save_character(character)
        return character.health
    
    if character.health > 0 and not fled: #What happens after the battle is over, and the enemy died (character not dead).
        print("\n*** The battle is over, and " + Fore.GREEN + Style.BRIGHT + f"{character.name}" + Fore.RESET + " has emerged victorious! ***\n")
        save_character(character)
        return character.health
    
    if fled:
        print(Fore.CYAN + f"\n*** {character.name} has successfully escaped the battle! ***\n")
    

my_acrobat = Acrobat(name = 'Nathan', age = 33, sex = 'male', height = 180) #These are just for testing the attack() function.

my_brawler = Brawler(name = 'Joseph', age = 35, sex = 'male', height = 183) #The attack() function will later be imported to main.py

my_academic = Academic(name = 'Samuel', age = 37, sex = 'male', height = 180) #And it will use the loaded character save to input data.

my_socialite = Socialite(name = 'Jeromy', age = 31, sex = 'male', height = 178)

my_elder = Elder(name = 'Coles', age = 31, sex = 'male', height = 178)

my_fortunate = Fortunate(name = 'Zach', age = 33, sex = 'male', height = 178)

enemy = Orc(name = 'Bork')

#attack(my_fortunate, enemy, enemy.difficulty)

#attack_choice(my_acrobat, enemy)



    
    