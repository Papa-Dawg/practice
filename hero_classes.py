##This file contains the hero classes, which the user can choose from.

class Acrobat:
    #These stats are inherent to the class.
    weapon = 'bowstaff'
    health = 100
    phys = 9
    inte = 3
    soc = 4
    luck = 6
    wis = 3

    #These stats are set when an object of the class is first initiated, like Zach the Fortunate.
    def __init__(self, name, age, sex, height):
        self.name = name
        self.age = age
        self.sex = sex
        self.height = height
    

class Brawler:

    weapon = 'brass knuckles'
    health = 100
    phys = 7
    inte = 5
    soc = 5
    luck = 4
    wis = 4

    def __init__(self, name, age, sex, height):
        self.name = name
        self.age = age
        self.sex = sex
        self.height = height


class Academic:

    weapon = 'bow and arrow'
    health = 100
    phys = 3
    inte = 9
    soc = 2
    luck = 5
    wis = 6

    def __init__(self, name, age, sex, height):
        self.name = name
        self.age = age
        self.sex = sex
        self.height = height


class Socialite:

    weapon = 'rapier'
    health = 100
    phys = 5
    inte = 5
    soc = 9
    luck = 5
    wis = 1

    def __init__(self, name, age, sex, height):
        self.name = name
        self.age = age
        self.sex = sex
        self.height = height


class Fortunate:

    weapon = 'surroundings'
    health = 100
    phys = 2
    inte = 4
    soc = 7
    luck = 9
    wis = 3

    def __init__(self, name, age, sex, height):
        self.name = name
        self.age = age
        self.sex = sex
        self.height = height


class Elder:

    weapon = 'pistol'
    health = 100
    phys = 1
    inte = 7
    soc = 5
    luck = 3
    wis = 9

    def __init__(self, name, age, sex, height):
        self.name = name
        self.age = age
        self.sex = sex
        self.height = height
