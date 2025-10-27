## This file just handles how the character data is saved.
## The data is updated to a file when saved, and can be updated from that file when loaded.

import json
import pickle
from colorama import Fore, Style, init

init(autoreset=True)

JSON_DATA_FILE = 'character_data.json'
DATA_FILE = 'character_data.bin'

def save_character_health(character):

    save_data = f'{character.name},{character.health}\n'

    updated_lines = []

    found_character = False

    try:
        with open('data.txt', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
    
        name, _ = line.split(',')

        if name == character.name:
            updated_lines.append(save_data)
            found_character = True
        else:
            updated_lines.append(line + '\n')
    
    if not found_character:
        updated_lines.append(save_data)
    
    try:
        with open('data.txt', 'w') as f:
            f.writelines(updated_lines)
            print(Fore.GREEN + Style.BRIGHT + f"\n{character.name}" + Fore.GREEN + "'s health has been saved.")
    except Exception as e:
        print(Fore.RED + f"Error, could not save: {e}")


def load_character(character):

    character_data = {}

    try:
        with open(JSON_DATA_FILE, 'r') as f:
            character_data.update(json.load(f))
            return character_data
    except FileNotFoundError:
        return {}
    except EOFError:
        return {}
    except Exception as e:
        print(Fore.RED + f"Error, could not load character from JSON file: {e}")
    try:
        with open(DATA_FILE, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}
    except EOFError:
        return {}
    except Exception as e:
        print(Fore.RED + f"Error, could not load character: {e}")


def load_all_character_data():
    
    try:
        with open(JSON_DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, EOFError):
        return {}

def save_character(character):
    
    all_character_data = load_all_character_data()

    character_info = {
        'name': character.name,
        'health': character.health,
        'weapon': character.weapon,
        'age': character.age,
        'sex': character.sex,
        'height': character.height,
        'phys': character.phys,
        'inte': character.inte,
        'soc': character.soc,
        'luck': character.luck,
        'wis': character.wis
    }
    
    all_character_data[character.name] = character_info

    try:
        with open(JSON_DATA_FILE, 'w') as f:
            json.dump(all_character_data, f, indent=4)
            print(Fore.GREEN + Style.BRIGHT + f"\n{character.name}" + Fore.GREEN + "'s stats have been saved to JSON file.")
    except Exception as e:
        print(Fore.RED + f"Error, could not save character to JSON file: {e}")

    try:
        with open(DATA_FILE, 'wb') as f:
            pickle.dump(all_character_data, f) 
            print(Fore.GREEN + Style.BRIGHT + f"\n{character.name}" + Fore.GREEN + "'s stats have been saved.")
    except Exception as e:
        print(Fore.RED + f"Error, could not save character: {e}")