## This page contains the current modifiers based on the character's stats. I'm sure these will change, lol.

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
