from .content import RECIPES
from .constants import clear_screen
from .models import Item
from .ui import print_table


class CraftingService:
    def __init__(self, player):
        self.player = player

    def craft(self):
        while True:
            clear_screen()
            print("\n=== CRAFTING ===")
            recipes = sorted(RECIPES.items(), key=lambda entry: entry[1]["name"].lower())
            print_table(
                ("#", "Recipe", "Ingredients"),
                [(key, recipe["name"], ", ".join(f"{name} x{amount}" for name, amount in recipe["cost"].items())) for key, recipe in recipes],
                (4, 30, 48),
            )
            choice = input("Choose a recipe, or 0 to return: ").strip()
            if choice in {"", "0"}:
                return
            if choice not in RECIPES:
                print("Invalid recipe choice.")
                input("Press Enter to continue: ")
                continue
            amount_text = input("Quantity [1]: ").strip()
            amount = int(amount_text) if amount_text.isdigit() and int(amount_text) > 0 else 1
            recipe = RECIPES[choice]
            if any(self.player.materials[name] < cost * amount for name, cost in recipe["cost"].items()):
                print("Not enough materials.")
                input("Press Enter to continue crafting: ")
                continue
            for name, cost in recipe["cost"].items():
                self.player.materials[name] -= cost * amount
            item = recipe["item"]
            self.player.add_item(Item(item.name, item.item_type, item.behavior, item.value, amount, item.rarity, item.grade, item.enchantment))
            print(f"Crafted {amount} {item.name}.")
            input("Press Enter to continue crafting: ")
