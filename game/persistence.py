import json
import os

from cryptography.fernet import Fernet, InvalidToken

from .constants import LEGACY_SAVE_FILE, MAPS, SAVE_FILE, SAVE_KEY_FILE, current_week_key
from .content import SKILLS, healing_potion
from .models import Item, Player

OLD_TYPES = {"Senjata": "Weapon", "Zirah": "Armor", "Ramuan": "Healing Potion", "Eksplorasi": "Exploration"}
OLD_MATERIALS = {"Herba": "Herb", "Serpihan Besi": "Iron Shard", "Inti Monster": "Monster Core"}
OLD_MAPS = {"1": "1", "2": "2", "3": "3"}
OLD_NAMES = {
    "Pedang Besi": "Iron Sword",
    "Tongkat Sihir": "Magic Staff",
    "Jubah Pelindung": "Protective Robe",
    "Ramuan Ajaib": "Healing Potion",
    "Potion Eksplorasi": "Exploration Potion",
}
OLD_RARITIES = {"[Langka]": "[Rare]", "[EPIK]": "[Epic]", "[LEGENDARIS]": "[Legendary]"}


def item_to_dict(item):
    return {
        "name": item.name,
        "item_type": item.item_type,
        "behavior": item.behavior,
        "value": item.value,
        "quantity": item.quantity,
        "rarity": item.rarity,
        "grade": item.grade,
        "enchantment": item.enchantment,
        "attack_bonus": item.attack_bonus,
        "defense_bonus": item.defense_bonus,
        "speed_bonus": item.speed_bonus,
        "crit_chance_bonus": item.crit_chance_bonus,
        "crit_damage_bonus": item.crit_damage_bonus,
    }


def item_from_dict(data):
    name = data.get("name", data.get("base_name", "Unknown Item"))
    for old_name, new_name in OLD_NAMES.items():
        name = name.replace(old_name, new_name)
    for old_rarity, new_rarity in OLD_RARITIES.items():
        name = name.replace(old_rarity, new_rarity)
    item_type = data.get("item_type", "Misc")
    item_type = OLD_TYPES.get(item_type, item_type)
    if item_type == "Exploration":
        migrated = healing_potion()
        name = migrated.name
        item_type = migrated.item_type
        behavior = migrated.behavior
        value = migrated.value
    else:
        behavior = data.get("behavior", "Misc")
        value = data.get("value", data.get("base_value", 0))
    rarity = data.get("rarity") or "Common"
    for known_rarity in ("Primordial", "Mythical", "Legendary", "Heroic", "Epic", "Rare", "Uncommon"):
        if known_rarity in name:
            rarity = known_rarity
            break
    return Item(
        name, item_type, behavior, value, data.get("quantity", 1), rarity,
        data.get("grade", "Standard"), data.get("enchantment", "None"),
        data.get("attack_bonus", 0), data.get("defense_bonus", 0),
        data.get("speed_bonus", 0), data.get("crit_chance_bonus", 0.0),
        data.get("crit_damage_bonus", 0.0),
    )


def save_player(player):
    data = {
        "version": 2,
        "level": player.level,
        "exp": player.exp,
        "gold": player.gold,
        "stats": player.stats,
        "turn_counter": player.turn_counter,
        "equipment": {slot: item_to_dict(item) if item else None for slot, item in player.equipment.items()},
        "inventory": [item_to_dict(item) for item in player.inventory],
        "active_skill": player.active_skill,
        "current_map": player.current_map,
        "week_key": player.week_key,
        "mobs_this_week": player.mobs_this_week,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "materials": player.materials,
        "encounters_since_miniboss": player.encounters_since_miniboss,
        "encounters_since_boss": player.encounters_since_boss,
    }
    key = _load_or_create_key()
    encrypted = Fernet(key).encrypt(json.dumps(data).encode("utf-8"))
    temporary_file = f"{SAVE_FILE}.tmp"
    with open(temporary_file, "wb") as save_file:
        save_file.write(encrypted)
    os.replace(temporary_file, SAVE_FILE)
    if os.path.exists(LEGACY_SAVE_FILE):
        os.remove(LEGACY_SAVE_FILE)


def _load_or_create_key():
    if os.path.exists(SAVE_KEY_FILE):
        with open(SAVE_KEY_FILE, "rb") as key_file:
            return key_file.read().strip()
    key = Fernet.generate_key()
    with open(SAVE_KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key


def _load_save_data():
    if os.path.exists(SAVE_FILE):
        key = _load_or_create_key()
        with open(SAVE_FILE, "rb") as save_file:
            return json.loads(Fernet(key).decrypt(save_file.read()).decode("utf-8"))
    if os.path.exists(LEGACY_SAVE_FILE):
        with open(LEGACY_SAVE_FILE, "r", encoding="utf-8") as save_file:
            return json.load(save_file)
    return None


def load_player():
    player = Player()
    player.skills = list(SKILLS)
    if not os.path.exists(SAVE_FILE) and not os.path.exists(LEGACY_SAVE_FILE):
        player.week_key = current_week_key()
        print("No save file found. Starting a new adventure.")
        return player
    try:
        data = _load_save_data()
        player.level = data.get("level", player.level)
        player.exp = data.get("exp", player.exp)
        player.gold = data.get("gold", player.gold)
        player.stats.update(data.get("stats", {}))
        player.turn_counter = data.get("turn_counter", 0)
        for slot, saved_item in data.get("equipment", {}).items():
            if saved_item:
                slot = {"Senjata": "Weapon", "Zirah": "Armor"}.get(slot, slot)
                if slot in player.equipment:
                    player.equipment[slot] = item_from_dict(saved_item)
        player.inventory = [item_from_dict(item) for item in data.get("inventory", [])]
        player.active_skill = min(data.get("active_skill", 0), len(player.skills) - 1)
        player.current_map = data.get("current_map", "1")
        player.current_map = OLD_MAPS.get(player.current_map, player.current_map)
        if player.current_map not in MAPS:
            player.current_map = "1"
        player.week_key = data.get("week_key", current_week_key())
        player.mobs_this_week = data.get("mobs_this_week", 0)
        player.max_hp = data.get("max_hp", 100 + (player.level - 1) * 10)
        player.hp = min(data.get("hp", player.max_hp), player.max_hp)
        for name, amount in data.get("materials", {}).items():
            player.materials[OLD_MATERIALS.get(name, name)] = amount
        player.encounters_since_miniboss = data.get("encounters_since_miniboss", 0)
        player.encounters_since_boss = data.get("encounters_since_boss", 0)
        if player.week_key != current_week_key():
            player.week_key = current_week_key()
            player.mobs_this_week = 0
        print("Save loaded successfully.")
    except (OSError, ValueError, TypeError, KeyError, InvalidToken):
        print("Save file could not be verified or loaded. Starting a new adventure.")
    return player
