from .constants import EQUIPMENT_SLOTS, RARITY_COLORS, color_text
from .models import Item


class InventoryService:
    def __init__(self, player, clear_screen):
        self.player = player
        self.clear_screen = clear_screen

    def _show_equipment(self):
        print("--- EQUIPPED GEAR ---")
        for slot in EQUIPMENT_SLOTS:
            item = self.player.equipment[slot]
            if item:
                rarity = color_text(item.rarity, RARITY_COLORS.get(item.rarity, ""))
                print(f"{slot:<11} [EQUIPPED] {item.name} | {rarity} | Power {item.value}")
            else:
                print(f"{slot:<11} -- empty --")

    def _show_bag(self):
        print("\n--- BAG ---")
        if not self.player.inventory:
            print("Bag is empty.")
            return
        for index, item in enumerate(self.player.inventory, 1):
            action = "equip" if item.item_type in EQUIPMENT_SLOTS else "use"
            grade = f" | {item.grade}" if item.item_type == "Healing Potion" else ""
            enchantment = f" | Enchant: {item.enchantment}" if item.enchantment != "None" else ""
            rarity = color_text(item.rarity, RARITY_COLORS.get(item.rarity, ""))
            print(f"{index}. {item.name} x{item.quantity} | {rarity}{grade} | {item.item_type} | Power {item.value}{enchantment} | {action}")

    def show_and_manage(self):
        while True:
            self.clear_screen()
            print("=== INVENTORY ===")
            self._show_equipment()
            self._show_bag()
            choice = input("\nChoose a bag item, or 0 to return: ").strip()
            if choice in {"", "0"}:
                return
            if not choice.isdigit() or not 1 <= int(choice) <= len(self.player.inventory):
                print("Invalid item choice.")
                input("Press Enter to continue: ")
                continue
            item = self.player.inventory[int(choice) - 1]
            if item.item_type in self.player.equipment:
                self._equip(item)
            elif item.item_type == "Healing Potion":
                self.player.remove_one_item(item)
                old_hp = self.player.hp
                self.player.heal(item.value)
                print(f"Used {item.name}: {old_hp} -> {self.player.hp} HP.")
            else:
                print("This item cannot be used here.")
            input("Press Enter to continue managing inventory: ")

    def _equip(self, item):
        slot = item.item_type
        self.player.remove_one_item(item)
        previous = self.player.equipment[slot]
        if previous:
            self.player.add_item(previous)
        self.player.equipment[slot] = Item(item.name, item.item_type, item.behavior, item.value, rarity=item.rarity, grade=item.grade, enchantment=item.enchantment)
        print(f"Equipped {item.name} in the {slot} slot.")
