from datetime import date
import os
import sys

SAVE_FILE = "savegame.json"
MAX_WEEKLY_MOBS = 100000
RANDOM_POTION_CHANCE = 0.01
COMBAT_ACTION_DELAY = 0.5
COMBAT_RESULT_DELAY = 2.0

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
GOLD = "\033[93m"
WHITE = "\033[97m"
GRAY = "\033[90m"
MAGENTA = "\033[95m"

RARITY_COLORS = {
    "Common": GRAY,
    "Uncommon": GREEN,
    "Rare": BLUE,
    "Epic": MAGENTA,
    "Heroic": "\033[91m",
    "Legendary": GOLD,
    "Mythical": "\033[96m",
    "Primordial": "\033[1;97m\033[45m",
}

RANK_COLORS = {"Normal": WHITE, "Miniboss": MAGENTA, "Boss": RED}
SKILL_CATEGORY_COLORS = {"Damage": RED, "Buff": GREEN, "Debuff": GOLD, "Control": BLUE, "Passive": CYAN, "Utility": WHITE, "Active": WHITE}


def color_text(text, color):
    return f"{color}{text}{RESET}"


def rarity_text(text, rarity):
    return color_text(text, RARITY_COLORS.get(rarity, WHITE))


def health_text(current, maximum):
    ratio = current / maximum if maximum else 0
    color = GREEN if ratio > 0.6 else GOLD if ratio > 0.3 else RED
    return color_text(f"{current}/{maximum}", color)

EQUIPMENT_SLOTS = ("Weapon", "Armor", "Helmet", "Gloves", "Boots", "Accessory")
ITEM_TYPE_ORDER = {slot: index for index, slot in enumerate(EQUIPMENT_SLOTS)}
ITEM_TYPE_ORDER.update({"Healing Potion": 20, "Misc": 30})
RARITY_ORDER = {
    "Common": 0,
    "Uncommon": 1,
    "Rare": 2,
    "Epic": 3,
    "Heroic": 4,
    "Legendary": 5,
    "Mythical": 6,
    "Primordial": 7,
}
SKILL_CATEGORY_ORDER = {"Damage": 0, "Buff": 1, "Debuff": 2, "Control": 3, "Passive": 4, "Utility": 5, "Active": 6}


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    print("\033[2J\033[3J\033[H", end="", flush=True)


def enter_pressed():
    if os.name == "nt":
        import msvcrt

        if not msvcrt.kbhit():
            return False
        return msvcrt.getwch() in {"\r", "\n"}
    import select

    ready, _, _ = select.select([sys.stdin], [], [], 0)
    if not ready:
        return False
    return sys.stdin.readline().strip() == ""

MAPS = {
    "1": {
        "name": "Grasslands",
        "difficulty": "Easy",
        "monster_level_bonus": 0,
        "rank_chances": {"Miniboss": 0.015, "Boss": 0.002},
        "miniboss_pity": 35,
        "boss_pity": 150,
        "monsters": ["Meadow Slime", "Wild Boar", "Grass Stalker", "Hill Goblin"],
    },
    "2": {
        "name": "Cursed Forest",
        "difficulty": "Hard",
        "monster_level_bonus": 2,
        "rank_chances": {"Miniboss": 0.03, "Boss": 0.006},
        "miniboss_pity": 30,
        "boss_pity": 120,
        "monsters": ["Thorn Hag", "Moss Troll", "Rotfang Spider", "Cursed Dryad"],
    },
    "3": {
        "name": "Dragon Crater",
        "difficulty": "Extreme",
        "monster_level_bonus": 5,
        "rank_chances": {"Miniboss": 0.05, "Boss": 0.012},
        "miniboss_pity": 25,
        "boss_pity": 90,
        "monsters": ["Ember Drake", "Magma Golem", "Ash Wyrm", "Cinder Revenant"],
    },
    "4": {
        "name": "Sunken Ruins",
        "difficulty": "Very Hard",
        "monster_level_bonus": 8,
        "rank_chances": {"Miniboss": 0.06, "Boss": 0.016},
        "miniboss_pity": 22,
        "boss_pity": 80,
        "monsters": ["Drowned Knight", "Abyssal Eel", "Tide Oracle", "Coral Warden"],
    },
    "5": {
        "name": "Storm Peaks",
        "difficulty": "Very Hard",
        "monster_level_bonus": 11,
        "rank_chances": {"Miniboss": 0.07, "Boss": 0.02},
        "miniboss_pity": 20,
        "boss_pity": 70,
        "monsters": ["Storm Roc", "Frost Giant", "Thunder Hound", "Sky Marauder"],
    },
    "6": {
        "name": "Void Frontier",
        "difficulty": "Nightmare",
        "monster_level_bonus": 15,
        "rank_chances": {"Miniboss": 0.09, "Boss": 0.03},
        "miniboss_pity": 15,
        "boss_pity": 50,
        "monsters": ["Void Stalker", "Null Wraith", "Reality Eater", "Starless Horror"],
    },
}


def current_week_key():
    calendar = date.today().isocalendar()
    return f"{calendar.year}-W{calendar.week:02d}"
