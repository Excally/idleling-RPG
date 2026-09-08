from .models import Item, Skill

POTION_GRADES = {
    "Standard": {"value": 100, "price": 25, "materials": {"Herb": 2, "Monster Core": 1}},
    "Greater": {"value": 250, "price": 60, "materials": {"Herb": 4, "Monster Core": 2}},
    "Superior": {"value": 500, "price": 140, "materials": {"Herb": 7, "Monster Core": 4}},
    "Masterwork": {"value": 900, "price": 300, "materials": {"Herb": 12, "Monster Core": 7}},
    "Transcendent": {"value": 1500, "price": 650, "materials": {"Herb": 20, "Monster Core": 12}},
}
HEALING_POTION_VALUE = POTION_GRADES["Standard"]["value"]


def healing_potion(grade="Standard", quantity=1):
    potion = POTION_GRADES[grade]
    return Item(f"{grade} Healing Potion", "Healing Potion", "Consume", potion["value"], quantity, "Common", grade)

SKILLS = [
    Skill("Lightning Slash", 0.20, 2.0, "casts LIGHTNING SLASH", "speed", 3, 2, False, "Buff"),
    Skill("Earthquake", 0.10, 3.5, "uses a devastating EARTHQUAKE", "defense_down", 0.2, 2, False, "Debuff"),
    Skill("Quick Strike", 0.30, 1.5, "lands a QUICK STRIKE", "speed", 5, 1, False, "Buff"),
    Skill("Shield Breaker", 0.16, 2.4, "uses SHIELD BREAKER", "defense_down", 0.25, 2, False, "Debuff"),
    Skill("Whirlwind", 0.12, 2.8, "spins through the enemy with WHIRLWIND", "double_strike", 0.15, 2, False, "Damage"),
    Skill("Venomous Cut", 0.18, 2.1, "delivers a VENOMOUS CUT", "damage_over_time", 0.08, 3, False, "Debuff"),
    Skill("Meteor Hammer", 0.08, 4.0, "brings down the METEOR HAMMER", "stun", 0, 1, False, "Control"),
    Skill("Frost Lance", 0.14, 2.6, "fires a FROST LANCE", "speed_down", 4, 2, False, "Debuff"),
    Skill("Shadow Fang", 0.11, 3.2, "strikes from the shadows with SHADOW FANG", "lifesteal", 0.2, 1, False, "Buff"),
    Skill("Arcane Burst", 0.09, 4.5, "releases an ARCANE BURST", "crit_up", 0.1, 2, False, "Buff"),
    Skill("Rending Claw", 0.22, 1.9, "tears through the target with RENDING CLAW", "bleed", 0.1, 3, False, "Debuff"),
    Skill("Solar Impact", 0.05, 6.0, "channels a devastating SOLAR IMPACT", "stun", 0, 1, False, "Control"),
    Skill("Battle Focus", 1.0, 1.0, "maintains BATTLE FOCUS", "passive_attack", 0.1, 0, True, "Passive"),
    Skill("Iron Will", 1.0, 1.0, "maintains IRON WILL", "passive_defense", 0.15, 0, True, "Passive"),
]

ENCHANTMENTS = {
    "Swift": "Adds speed based on gear power.",
    "Berserker": "Deals 15% more damage below 40% HP.",
    "Double Strike": "Has a chance to attack twice.",
    "Vampiric": "Restores a portion of damage dealt.",
    "Bulwark": "Reduces incoming damage.",
    "Focused": "Increases critical chance.",
}

BASE_ITEMS = [
    Item("Iron Sword", "Weapon", "Equip", 10),
    Item("Magic Staff", "Weapon", "Equip", 12),
    Item("Steel Longsword", "Weapon", "Equip", 15),
    Item("Hunter Bow", "Weapon", "Equip", 14),
    Item("Battle Axe", "Weapon", "Equip", 18),
    Item("Spear of Dawn", "Weapon", "Equip", 20),
    Item("Runic Blade", "Weapon", "Equip", 24),
    Item("Gravecleaver", "Weapon", "Equip", 28),
    Item("Stormcaller", "Weapon", "Equip", 32),
    Item("Void Edge", "Weapon", "Equip", 38),
    Item("Protective Robe", "Armor", "Equip", 8),
    Item("Chainmail Vest", "Armor", "Equip", 11),
    Item("Knight Breastplate", "Armor", "Equip", 16),
    Item("Warden Armor", "Armor", "Equip", 21),
    Item("Astral Mantle", "Armor", "Equip", 26),
    Item("Abyssal Plate", "Armor", "Equip", 31),
    Item("Stormguard Cuirass", "Armor", "Equip", 36),
    Item("Voidweave Raiment", "Armor", "Equip", 44),
    Item("Iron Helmet", "Helmet", "Equip", 6),
    Item("Steel Helm", "Helmet", "Equip", 9),
    Item("Knight Sallet", "Helmet", "Equip", 13),
    Item("Dragon Crown", "Helmet", "Equip", 19),
    Item("Tideforged Helm", "Helmet", "Equip", 24),
    Item("Storm Crown", "Helmet", "Equip", 29),
    Item("Void Visage", "Helmet", "Equip", 35),
    Item("Leather Gloves", "Gloves", "Equip", 5),
    Item("Steel Gauntlets", "Gloves", "Equip", 8),
    Item("Duelist Grips", "Gloves", "Equip", 12),
    Item("Titan Gauntlets", "Gloves", "Equip", 17),
    Item("Coral Fists", "Gloves", "Equip", 22),
    Item("Stormgrip Gauntlets", "Gloves", "Equip", 27),
    Item("Nullweave Gloves", "Gloves", "Equip", 33),
    Item("Traveler Boots", "Boots", "Equip", 5),
    Item("Steel Greaves", "Boots", "Equip", 8),
    Item("Windrunner Boots", "Boots", "Equip", 12),
    Item("Titan Treads", "Boots", "Equip", 17),
    Item("Tidewalker Boots", "Boots", "Equip", 22),
    Item("Stormstep Greaves", "Boots", "Equip", 27),
    Item("Voidwalker Treads", "Boots", "Equip", 33),
    Item("Silver Ring", "Accessory", "Equip", 7),
    Item("Ruby Pendant", "Accessory", "Equip", 9),
    Item("Emerald Charm", "Accessory", "Equip", 11),
    Item("Sapphire Sigil", "Accessory", "Equip", 14),
    Item("Dragon Eye", "Accessory", "Equip", 18),
    Item("Crown of Stars", "Accessory", "Equip", 23),
    Item("Pearl of the Deep", "Accessory", "Equip", 28),
    Item("Eye of the Storm", "Accessory", "Equip", 34),
    Item("Voidheart Shard", "Accessory", "Equip", 42),
    healing_potion(),
]

SHOP_ITEMS = {
    "1": {"name": "Standard Healing Potion", "item": healing_potion(), "price": POTION_GRADES["Standard"]["price"]},
    "2": {"name": "Greater Healing Potion", "item": healing_potion("Greater"), "price": POTION_GRADES["Greater"]["price"]},
    "3": {"name": "Superior Healing Potion", "item": healing_potion("Superior"), "price": POTION_GRADES["Superior"]["price"]},
    "4": {"name": "Herb", "material": "Herb", "price": 10},
    "5": {"name": "Iron Shard", "material": "Iron Shard", "price": 20},
}

RECIPES = {
    "1": {"name": "Standard Healing Potion", "cost": POTION_GRADES["Standard"]["materials"], "item": healing_potion()},
    "2": {"name": "Greater Healing Potion", "cost": POTION_GRADES["Greater"]["materials"], "item": healing_potion("Greater")},
    "3": {"name": "Superior Healing Potion", "cost": POTION_GRADES["Superior"]["materials"], "item": healing_potion("Superior")},
    "4": {"name": "Masterwork Healing Potion", "cost": POTION_GRADES["Masterwork"]["materials"], "item": healing_potion("Masterwork")},
    "5": {"name": "Forged Iron Sword", "cost": {"Iron Shard": 3, "Monster Core": 2}, "item": Item("Forged Iron Sword", "Weapon", "Equip", 18)},
}

ITEM_TIERS = [
    {"name": "Common", "multiplier": 1.0, "weight": 650, "label": "Common"},
    {"name": "Uncommon", "multiplier": 1.2, "weight": 180, "label": "Uncommon"},
    {"name": "Rare", "multiplier": 1.5, "weight": 90, "label": "Rare"},
    {"name": "Epic", "multiplier": 2.2, "weight": 45, "label": "Epic"},
    {"name": "Heroic", "multiplier": 3.0, "weight": 20, "label": "Heroic"},
    {"name": "Legendary", "multiplier": 4.0, "weight": 10, "label": "Legendary"},
    {"name": "Mythical", "multiplier": 6.0, "weight": 4, "label": "Mythical"},
    {"name": "Primordial", "multiplier": 9.0, "weight": 1, "label": "Primordial"},
]

DROP_RATE_REFERENCE = [
    ("Common", "65.0%"),
    ("Uncommon", "18.0%"),
    ("Rare", "9.0%"),
    ("Epic", "4.5%"),
    ("Heroic", "2.0%"),
    ("Legendary", "1.0%"),
    ("Mythical", "0.4%"),
    ("Primordial", "0.1%"),
]
