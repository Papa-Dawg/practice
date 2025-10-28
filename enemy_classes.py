## This file handles the various enemy classes

class Orc:
    #These stats below are inherent to the class.
    species = 'Orc'
    health = 50
    phys = 3
    inte = 3
    soc = 3
    luck = 3
    wis = 3

    flee = 50 #Out of 100. Higher number = Harder to flee.

    #These stats below are chosen when created an object of a certain class, like Bork the Orc. More will be added, I'm sure.
    def __init__(self, name):
        self.name = name

