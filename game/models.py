from dataclasses import dataclass
@dataclass
class Item:
    name: str
    item_type: str
    behavior: str
    value: int
    quantity: int = 1
    rarity: str = "Common"
    grade: str = "Standard"
    enchantment: str = "None"
    attack_bonus: int = 0
    defense_bonus: int = 0
    speed_bonus: int = 0
    crit_chance_bonus: float = 0.0
    crit_damage_bonus: float = 0.0

    def __post_init__(self):
        if self.item_type == "Weapon" and self.attack_bonus == 0:
            self.attack_bonus = self.value
        elif self.item_type == "Armor" and self.defense_bonus == 0:
            self.defense_bonus = self.value // 2
        elif self.item_type == "Helmet" and self.defense_bonus == 0:
            self.defense_bonus = self.value // 3
        elif self.item_type == "Gloves" and self.crit_chance_bonus == 0:
            self.crit_chance_bonus = self.value / 200
        elif self.item_type == "Boots" and self.speed_bonus == 0:
            self.speed_bonus = self.value // 2
        elif self.item_type == "Accessory" and self.attack_bonus == 0:
            self.attack_bonus = self.value // 2
            self.defense_bonus = self.value // 3
            self.crit_damage_bonus = self.value / 100


@dataclass
class Skill:
    name: str
    proc_chance: float
    damage_multiplier: float
    effect_text: str
    buff_type: str = "None"
    buff_value: float = 0.0
    buff_duration: int = 0
    passive: bool = False
    category: str = "Active"


@dataclass
class Monster:
    name: str
    hp: int
    exp: int
    gold: int
    attack: int
    is_boss: bool = False
    rank: str = "Normal"
    speed: int = 10
    defense: int = 0
    dodge_chance: float = 0.0


class Player:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.stats = {"ATK": 10, "CRIT_CHANCE": 0.05, "CRIT_DMG": 1.5}
        self.equipment = {
            "Weapon": None,
            "Armor": None,
            "Helmet": None,
            "Gloves": None,
            "Boots": None,
            "Accessory": None,
        }
        self.inventory = []
        self.skills = []
        self.active_skill = 0
        self.turn_counter = 0
        self.current_map = "1"
        self.week_key = ""
        self.mobs_this_week = 0
        self.hp = 100
        self.max_hp = 100
        self.materials = {"Herb": 0, "Iron Shard": 0, "Monster Core": 0}
        self.session_encounters = 0
        self.encounters_since_miniboss = 0
        self.encounters_since_boss = 0

    def total_attack(self):
        attack = self.stats["ATK"]
        attack += sum(gear.attack_bonus for gear in self.equipment.values() if gear)
        return int(attack * (1.15 if self.has_enchantment("Berserker") and self.hp <= self.max_hp * 0.4 else 1.0))

    def total_defense(self):
        defense_slots = ("Armor", "Helmet", "Gloves", "Boots", "Accessory")
        return self.stats.get("DEF", 0) + sum(self.equipment[slot].defense_bonus for slot in defense_slots if self.equipment[slot])

    def total_speed(self):
        speed = self.stats.get("SPEED", 10)
        return speed + sum(gear.speed_bonus for gear in self.equipment.values() if gear)

    def total_crit_chance(self):
        return min(1.0, self.stats["CRIT_CHANCE"] + sum(gear.crit_chance_bonus for gear in self.equipment.values() if gear))

    def total_crit_damage(self):
        return self.stats["CRIT_DMG"] + sum(gear.crit_damage_bonus for gear in self.equipment.values() if gear)

    def has_enchantment(self, enchantment):
        return any(gear and gear.enchantment == enchantment for gear in self.equipment.values())

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def add_item(self, item):
        for stored in self.inventory:
            if (stored.name, stored.item_type, stored.value, stored.rarity, stored.grade, stored.enchantment) == (item.name, item.item_type, item.value, item.rarity, item.grade, item.enchantment):
                stored.quantity += item.quantity
                return
        self.inventory.append(item)

    def remove_one_item(self, item):
        item.quantity -= 1
        if item.quantity <= 0:
            self.inventory.remove(item)

    def find_item(self, item_type):
        return next((item for item in self.inventory if item.item_type == item_type), None)

    def strongest_item(self, item_type):
        matching_items = [item for item in self.inventory if item.item_type == item_type]
        return max(matching_items, key=lambda item: item.value, default=None)
