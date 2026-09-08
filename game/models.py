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
        weapon = self.equipment["Weapon"]
        accessory = self.equipment["Accessory"]
        accessory_attack = accessory.value // 2 if accessory else 0
        attack = self.stats["ATK"] + (weapon.value if weapon else 0) + accessory_attack
        return int(attack * (1.15 if self.has_enchantment("Berserker") and self.hp <= self.max_hp * 0.4 else 1.0))

    def total_defense(self):
        defense_slots = ("Armor", "Helmet", "Gloves", "Boots", "Accessory")
        return sum(self.equipment[slot].value // 2 for slot in defense_slots if self.equipment[slot])

    def total_speed(self):
        speed = self.stats.get("SPEED", 10)
        return speed + sum(gear.value // 4 for gear in self.equipment.values() if gear and gear.enchantment == "Swift")

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
