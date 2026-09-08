import random

from .content import BASE_ITEMS, ENCHANTMENTS, ITEM_TIERS
from .models import Item


def generate_item():
    base = random.choice(BASE_ITEMS)
    tier = random.choices(ITEM_TIERS, weights=[entry["weight"] for entry in ITEM_TIERS])[0]
    prefix = "" if tier["name"] == "Common" else f"[{tier['label']}] "
    value = int(base.value * tier["multiplier"])
    enchantment = "None"
    if base.item_type not in {"Healing Potion"} and random.random() < 0.35:
        enchantment = random.choice(list(ENCHANTMENTS))
    enchantment_label = "" if enchantment == "None" else f" of {enchantment}"
    return Item(f"{prefix}{base.name}{enchantment_label}", base.item_type, base.behavior, value, rarity=tier["name"], enchantment=enchantment)
