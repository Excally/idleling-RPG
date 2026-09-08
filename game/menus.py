from .constants import EQUIPMENT_SLOTS, MAPS, MAX_WEEKLY_MOBS, SKILL_CATEGORY_COLORS, clear_screen, color_text


class MenuService:
    """Terminal UI only; game rules belong to the feature services."""

    def __init__(self, player, player_service, inventory_service, shop_service, crafting_service, exploration_service):
        self.player = player
        self.player_service = player_service
        self.inventory = inventory_service
        self.shop = shop_service
        self.crafting = crafting_service
        self.exploration = exploration_service

    def dashboard(self):
        return f"Level {self.player.level} | HP {self.player.hp}/{self.player.max_hp} | Gold {self.player.gold} | Map: {MAPS[self.player.current_map]['name']}"

    def show_status(self):
        item_count = sum(item.quantity for item in self.player.inventory)
        print("\n--- CHARACTER ---")
        print(f"Level {self.player.level} | HP {self.player.hp}/{self.player.max_hp} | Gold {self.player.gold}")
        print(f"ATK {self.player.total_attack()} | DEF {self.player.total_defense()} | XP {self.player.exp}")
        print("Gear: " + " | ".join(
            f"{slot}: {self.player.equipment[slot].name if self.player.equipment[slot] else '--'}"
            for slot in EQUIPMENT_SLOTS
        ))
        print("\n--- WORLD ---")
        print(f"Map: {MAPS[self.player.current_map]['name']}")
        print(f"Weekly progress: {self.player.mobs_this_week:,}/{MAX_WEEKLY_MOBS:,} mobs")
        map_data = MAPS[self.player.current_map]
        print(f"Pity: miniboss {self.player.encounters_since_miniboss}/{map_data['miniboss_pity']} | boss {self.player.encounters_since_boss}/{map_data['boss_pity']}")
        print("Materials: " + " | ".join(f"{name} {amount}" for name, amount in self.player.materials.items()))
        print(f"Inventory: {item_count} items in {len(self.player.inventory)} stacks")

    def choose_map(self):
        print("\n--- CHOOSE MAP ---")
        for key, map_data in MAPS.items():
            marker = "ACTIVE" if key == self.player.current_map else ""
            monsters = ", ".join(map_data["monsters"])
            print(f"{key}. {map_data['name']} | {map_data['difficulty']} | monsters: {monsters}")
            print(f"   Rank chance: miniboss {map_data['rank_chances']['Miniboss']:.1%}, boss {map_data['rank_chances']['Boss']:.1%} | pity {map_data['miniboss_pity']}/{map_data['boss_pity']} {marker}")
        choice = input("Map number, or Enter to cancel: ").strip()
        if choice in MAPS:
            self.player.current_map = choice
            print(f"Map changed to {MAPS[choice]['name']}.")
            input("Press Enter to continue: ")

    def choose_skill(self):
        while True:
            clear_screen()
            print("\n--- SKILLS ---")
            for index, skill in enumerate(self.player.skills, 1):
                marker = "ACTIVE" if index - 1 == self.player.active_skill else ""
                category = color_text(skill.category, SKILL_CATEGORY_COLORS.get(skill.category, ""))
                print(f"{index}. {skill.name} | {category} | {skill.proc_chance:.0%} chance | x{skill.damage_multiplier} damage {marker}")
            choice = input("Skill number, or 0 to return: ").strip()
            if choice in {"", "0"}:
                return
            if choice.isdigit() and 1 <= int(choice) <= len(self.player.skills):
                self.player.active_skill = int(choice) - 1
                print(f"Active skill: {self.player.skills[self.player.active_skill].name}.")
                input("Press Enter to continue managing skills: ")

    def train(self):
        while True:
            clear_screen()
            print("\n--- TRAINING ---")
            print("1. ATK +1 (10 gold)")
            print("2. Max HP +10 (15 gold)")
            choice = input("Training choice, or 0 to return: ").strip()
            if choice in {"", "0"}:
                return
            amount_text = input("Number of upgrades [1, max]: ").strip().lower()
            amount = 10**9 if amount_text == "max" else int(amount_text) if amount_text.isdigit() and int(amount_text) > 0 else 1
            _, message = self.player_service.upgrade_stat(choice, amount)
            print(message)
            input("Press Enter to continue training: ")

    def full_heal(self):
        if self.player.gold < 20:
            print("Full healing costs 20 gold.")
            return
        self.player.gold -= 20
        self.player.hp = self.player.max_hp
        print(f"HP restored to {self.player.hp}/{self.player.max_hp}.")

    def manage_menu(self):
        while True:
            clear_screen()
            print("\n=== MANAGE CHARACTER ===")
            print("1. Inventory")
            print("2. Skills")
            print("3. Training")
            print("0. Back")
            choice = input("Choice: ").strip()
            if choice == "1":
                self.inventory.show_and_manage()
            elif choice == "2":
                self.choose_skill()
            elif choice == "3":
                self.train()
            elif choice == "0":
                return
            else:
                print("Choose one of the listed options.")

    def town_menu(self):
        while True:
            clear_screen()
            print("\n=== TOWN ===")
            print("1. Shop")
            print("2. Crafting")
            print("3. Restore HP (20 gold)")
            print("0. Back")
            choice = input("Choice: ").strip()
            if choice == "1":
                self.shop.buy()
            elif choice == "2":
                self.crafting.craft()
            elif choice == "3":
                self.full_heal()
                input("Press Enter to continue: ")
            elif choice == "0":
                return
            else:
                print("Choose one of the listed options.")

    def run(self):
        while True:
            self.player_service.reset_week_if_needed()
            clear_screen()
            print("\n=== ADVENTURE ===")
            print(self.dashboard())
            print("1. Explore")
            print("2. Manage Character")
            print("3. Town")
            print("4. Change Map")
            print("5. View Status")
            print("0. Save and Exit")
            choice = input("Choice: ").strip()
            if choice == "1":
                self.exploration.run_session()
            elif choice == "2":
                self.manage_menu()
            elif choice == "3":
                self.town_menu()
            elif choice == "4":
                self.choose_map()
            elif choice == "5":
                self.show_status()
            elif choice == "0":
                return
            else:
                print("Choose one of the listed options.")
