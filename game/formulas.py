import random


def roll_damage(attack, crit_chance, crit_damage):
    critical = random.random() < crit_chance
    if critical:
        return int(attack * crit_damage), True
    return int(attack * random.uniform(0.9, 1.1)), False


def experience_needed(level):
    return int(100 * level ** 1.5)
