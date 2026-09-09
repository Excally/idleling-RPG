import random

from .constants import RARITY_ORDER
from .content import BASE_ITEMS, ENCHANTMENTS, ITEM_TIERS
from .models import Item


def generate_item(max_item_power=None, max_item_rarity="Primordial"):
    available_items = [item for item in BASE_ITEMS if max_item_power is None or item.value <= max_item_power]
    if not available_items:
        available_items = BASE_ITEMS
    available_tiers = [tier for tier in ITEM_TIERS if RARITY_ORDER[tier["name"]] <= RARITY_ORDER[max_item_rarity]]
    base = random.choice(available_items)
    tier = random.choices(available_tiers, weights=[entry["weight"] for entry in available_tiers])[0]
    value = int(base.value * tier["multiplier"])
    enchantment = "None"
    if base.item_type not in {"Healing Potion"} and random.random() < 0.35:
        enchantment = random.choice(list(ENCHANTMENTS))
    enchantment_label = "" if enchantment == "None" else f" of {enchantment}"
    return Item(f"{base.name}{enchantment_label}", base.item_type, base.behavior, value, rarity=tier["name"], enchantment=enchantment)
