from .constants import EQUIPMENT_SLOTS, ITEM_TYPE_ORDER, RARITY_ORDER, color_text, rarity_text
from .models import Item
from .ui import print_table, show_detail


class InventoryService:
    def __init__(self, player, clear_screen):
        self.player = player
        self.clear_screen = clear_screen

    def _show_equipment(self):
        print("--- EQUIPPED GEAR ---")
        for slot in EQUIPMENT_SLOTS:
            item = self.player.equipment[slot]
            if item:
                display_name = rarity_text(item.name, item.rarity)
                rarity = rarity_text(item.rarity, item.rarity)
                print(f"{slot:<11} [EQUIPPED] {display_name} | {rarity} | Power {item.value}")
            else:
                print(f"{slot:<11} -- empty --")

    def _sorted_inventory(self, sort_mode):
        if sort_mode == "name":
            return sorted(self.player.inventory, key=lambda item: item.name.lower())
        if sort_mode == "rarity":
            return sorted(self.player.inventory, key=lambda item: (-RARITY_ORDER.get(item.rarity, 0), item.name.lower()))
        if sort_mode == "power":
            return sorted(self.player.inventory, key=lambda item: (-item.value, item.name.lower()))
        return sorted(self.player.inventory, key=lambda item: (ITEM_TYPE_ORDER.get(item.item_type, 99), -item.value, item.name.lower()))

    def _item_stats(self, item):
        stats = []
        for label, value in (
            ("ATK", item.attack_bonus),
            ("DEF", item.defense_bonus),
            ("SPD", item.speed_bonus),
            ("CRIT", f"{item.crit_chance_bonus:.0%}"),
        ):
            if value != 0 and value != "0%":
                stats.append(f"{label} {value:+}" if label != "CRIT" else f"{label} {value}")
        return " | ".join(stats) if stats else "No combat stats"

    def _show_bag(self, items):
        print("\n--- BAG ---")
        if not self.player.inventory:
            print("Bag is empty.")
            return
        grouped = {}
        for item in items:
            section = "Consumables" if item.item_type == "Healing Potion" else item.item_type
            grouped.setdefault(section, []).append(item)
        index = 1
        rows = []
        item_lookup = {}
        section_order = list(EQUIPMENT_SLOTS) + ["Consumables", "Misc"]
        for section in section_order:
            if section not in grouped:
                continue
            for item in grouped[section]:
                action = "equip" if item.item_type in EQUIPMENT_SLOTS else "use"
                display_name = rarity_text(item.name, item.rarity)
                rarity = rarity_text(item.rarity, item.rarity)
                if item.item_type == "Healing Potion":
                    stats = f"{item.grade}, heals {item.value} HP"
                else:
                    enchantment = f" | {item.enchantment}" if item.enchantment != "None" else ""
                    stats = f"{self._item_stats(item)}{enchantment}"
                rows.append((index, display_name, item.item_type, rarity, item.quantity, stats, action))
                item_lookup[index] = item
                index += 1
        print_table(("#", "Item", "Type", "Rarity", "Qty", "Stats", "Use"), rows, (4, 28, 14, 12, 5, 28, 8))
        return item_lookup

    def show_and_manage(self):
        sort_mode = "type"
        while True:
            self.clear_screen()
            print("=== INVENTORY ===")
            self._show_equipment()
            sorted_items = self._sorted_inventory(sort_mode)
            item_lookup = self._show_bag(sorted_items)
            print(f"Sort: {sort_mode} | Commands: number=equip/use, S=sort, 0=return")
            choice = input("Choice: ").strip().lower()
            if choice in {"", "0"}:
                return
            if choice == "s":
                sort_choice = input("Sort by: 1 Type, 2 Name, 3 Rarity, 4 Power, 0 Cancel: ").strip()
                sort_mode = {"1": "type", "2": "name", "3": "rarity", "4": "power"}.get(sort_choice, sort_mode)
                continue
            if not choice.isdigit() or int(choice) not in item_lookup:
                print("Invalid item choice.")
                input("Press Enter to continue: ")
                continue
            item = item_lookup[int(choice)]
            if item.item_type in self.player.equipment:
                self._equip(item)
            elif item.item_type == "Healing Potion":
                self.player.remove_one_item(item)
                old_hp = self.player.hp
                self.player.heal(item.value)
                print(f"Used {item.name}: {old_hp} -> {self.player.hp} HP.")
                input("Press Enter to continue: ")
            else:
                print("This item cannot be used here.")
                input("Press Enter to continue: ")

    def _equip(self, item):
        slot = item.item_type
        self.player.remove_one_item(item)
        previous = self.player.equipment[slot]
        if previous:
            self.player.add_item(previous)
        self.player.equipment[slot] = Item(item.name, item.item_type, item.behavior, item.value, rarity=item.rarity, grade=item.grade, enchantment=item.enchantment)
        print(f"Equipped {item.name} in the {slot} slot.")
