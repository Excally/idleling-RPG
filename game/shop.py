from .content import SHOP_ITEMS
from .constants import clear_screen
from .models import Item
from .ui import print_table


class ShopService:
    def __init__(self, player):
        self.player = player

    def buy(self):
        while True:
            clear_screen()
            print("\n=== SHOP ===")
            products = sorted(SHOP_ITEMS.items(), key=lambda entry: (entry[1]["price"], entry[1]["name"].lower()))
            print_table(
                ("#", "Product", "Price", "Type"),
                [(key, product["name"], f"{product['price']} gold", "Material" if "material" in product else product["item"].item_type) for key, product in products],
                (4, 30, 14, 18),
            )
            choice = input("Choose an item, or 0 to return: ").strip()
            if choice in {"", "0"}:
                return
            if choice not in SHOP_ITEMS:
                print("Invalid shop choice.")
                input("Press Enter to continue: ")
                continue
            product = SHOP_ITEMS[choice]
            amount_text = input("Quantity [1, max]: ").strip().lower()
            amount = self.player.gold // product["price"] if amount_text == "max" else int(amount_text) if amount_text.isdigit() and int(amount_text) > 0 else 1
            total_price = product["price"] * amount
            if amount == 0 or self.player.gold < total_price:
                print("Not enough gold.")
                input("Press Enter to continue shopping: ")
                continue
            self.player.gold -= total_price
            if "material" in product:
                self.player.materials[product["material"]] += amount
            else:
                item = product["item"]
                self.player.add_item(Item(item.name, item.item_type, item.behavior, item.value, amount, item.rarity, item.grade, item.enchantment))
            print(f"Bought {amount} {product['name']}.")
            input("Press Enter to continue shopping: ")
