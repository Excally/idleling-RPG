import random

from .models import Monster

MONSTER_RANKS = {
    "Normal": {"hp": 1.0, "attack": 1.0, "reward": 1.0},
    "Miniboss": {"hp": 2.5, "attack": 1.6, "reward": 3.0},
    "Boss": {"hp": 6.0, "attack": 2.5, "reward": 10.0},
}
RANK_ORDER = {"Normal": 0, "Miniboss": 1, "Boss": 2}


def _rank_for_encounter(map_data, encounters_since_miniboss, encounters_since_boss):
    chances = map_data["rank_chances"]
    max_rank = map_data["max_monster_rank"]
    if RANK_ORDER[max_rank] >= RANK_ORDER["Boss"] and encounters_since_boss >= map_data["boss_pity"]:
        return "Boss", "Boss pity triggered"
    if RANK_ORDER[max_rank] >= RANK_ORDER["Miniboss"] and encounters_since_miniboss >= map_data["miniboss_pity"]:
        return "Miniboss", "Miniboss pity triggered"
    if RANK_ORDER[max_rank] >= RANK_ORDER["Boss"] and random.random() < chances["Boss"]:
        return "Boss", "Boss chance triggered"
    if RANK_ORDER[max_rank] >= RANK_ORDER["Miniboss"] and random.random() < chances["Miniboss"]:
        return "Miniboss", "Miniboss chance triggered"
    return "Normal", "Normal encounter"


def generate_monster(player_level, map_data, encounters_since_miniboss, encounters_since_boss):
    rank, trigger = _rank_for_encounter(map_data, encounters_since_miniboss, encounters_since_boss)
    rank_stats = MONSTER_RANKS[rank]
    monster_level = max(1, player_level + map_data["monster_level_bonus"])
    name = random.choice(map_data["monsters"])
    if rank == "Boss":
        name = f"{random.choice(['Ancient', 'Dread', 'Apex'])} {name} Overlord"
    elif rank == "Miniboss":
        name = f"Elite {name}"
    hp = int(30 * monster_level ** 1.1 * rank_stats["hp"])
    attack = int(5 * monster_level ** 1.1 * rank_stats["attack"])
    exp = int(20 * monster_level * rank_stats["reward"])
    gold = int(10 * monster_level * rank_stats["reward"])
    speed = max(5, int(10 + monster_level * 0.8 + (5 if rank == "Miniboss" else 10 if rank == "Boss" else 0)))
    defense = int(monster_level * (1 if rank == "Normal" else 2 if rank == "Miniboss" else 4))
    dodge_chance = 0.05 if rank == "Normal" else 0.08 if rank == "Miniboss" else 0.12
    return Monster(name, hp, exp, gold, attack, rank == "Boss", rank, speed, defense, dodge_chance), trigger
