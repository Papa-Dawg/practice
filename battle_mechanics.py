## This file handles the battle mechanics.

#Allows me to create different colored text output.
from colorama import Fore, Style, init

#Imports functions and classes from other files to use in the functions in this file.
from hero_classes import Acrobat, Fortunate, Brawler, Academic, Socialite, Elder
from enemy_classes import Orc
from roll_mechanics import dice_roll, weapon_damage
from modifiers import roll_add, damage_modifier
from data_save import save_character_health, save_character

init(autoreset=True) #Resets the color I add after every printed line. It would color everything after, otherwise.


def attack_choice(character, enemy): #Gives choice between actions on what to do next.
    
    print(
        "\n======== Next? ========\n" +
        f"1) Use {character.weapon}\n" +
        "2) Use item\n" +
        f"3) Confuse {enemy.name}\n" +
        "4) Flee\n"
        )
    
    choice = '' #Sets the choice to an empty string, so that it won't be considered valid.
    valid_choices = ['1', '2', '3,', '4'] #Sets what options are valid.
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

def flee(character, enemy): #Code for flee attempt (not done)
    base_chance_of_flee = int(dice_roll(100, 1)[0])
    luck_bonus = int(roll_add(character.luck))
    chance_of_flee = base_chance_of_flee + luck_bonus
    if chance_of_flee >= enemy.flee:
        return True
    else:
        return False

def attack(character, enemy, difficulty): #Initiates a battle to the death between the character and the enemy. Difficulty determined by enemy stat.

    print(Fore.RED + f"!!! " + Fore.GREEN + f"{character.name}" + Fore.RESET + " has encountered " + Fore.RED + f"{enemy.name} the {enemy.species} !!!")

    roll_bonus = roll_add(character.luck) #Uses the roll function, and adds a small amount to the roll based on the character's luck.
    damage_bonus = damage_modifier(character.phys) #Uses the damage modifier function, which creates a multiplier based on the character's phys stat.

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
                    print(f"{enemy.name} has {enemy.health} health remaining.")
            elif attack_attempt >= difficulty and critical: #Similar to above, but includes a "*2" multiplier when the hit is critical.
                enemy_health, damage = critical_attack(character, enemy, damage_bonus)
                if enemy_health <= 0:
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
        
        elif choice == '2': #Code for what happens if user chooses to use an item.
            pass
        elif choice == '3': #Code for what happens if user chooses to try to confuse the enemy.
            pass
        elif choice == '4': #Code for what happens if use tries to flee from the battle.
            chance_of_flee = flee(character, enemy)
            if chance_of_flee:
                fled = True
                break
            else:
                fled = False


    if enemy.health > 0 and not fled: #What happens after the battle is over, and the hero died (enemy not dead).
        print("\n*** The battle is over, and " + Fore.RED + Style.BRIGHT + f"{enemy.name}" + Fore.RESET + " has emerged victorious! ***\n")
        save_character_health(character)
        save_character(character)
        return character.health
    
    if character.health > 0 and not fled: #What happens after the battle is over, and the enemy died (character not dead).
        print("\n*** The battle is over, and " + Fore.GREEN + Style.BRIGHT + f"{character.name}" + Fore.RESET + " has emerged victorious! ***\n")
        save_character_health(character)
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

attack(my_fortunate, enemy, 15)

#attack_choice(my_acrobat, enemy)



    
    