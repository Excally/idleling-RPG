import random
import time

from .constants import COMBAT_RESULT_DELAY, MAPS, MAX_WEEKLY_MOBS, RANK_COLORS, clear_screen, color_text, enter_pressed, rarity_text
from .content import DROP_RATE_REFERENCE, healing_potion
from .items import generate_item
from .monsters import generate_monster


class ExplorationService:
    def __init__(self, player, player_service, combat_service, save_callback):
        self.player = player
        self.player_service = player_service
        self.combat_service = combat_service
        self.save_callback = save_callback

    def add_material_drop(self):
        material = random.choices(list(self.player.materials), weights=[5, 3, 2])[0]
        amount = random.randint(1, 2)
        self.player.materials[material] += amount
        print(f"Material drop: +{amount} {material}")

    def choose_map(self):
        print("\n--- EXPEDITION MAP ---")
        for key, map_data in MAPS.items():
            print(f"{key}. {map_data['name']} | {map_data['difficulty']} | monster level +{map_data['monster_level_bonus']}")
        choice = input("Choose a map for this expedition: ").strip()
        if choice not in MAPS:
            print("Invalid map. Expedition cancelled.")
            return None
        self.player.current_map = choice
        map_data = MAPS[choice]
        print(f"Map selected: {map_data['name']} ({map_data['difficulty']}).")
        print("Item tiers: " + " | ".join(f"{tier} {chance}" for tier, chance in DROP_RATE_REFERENCE))
        return map_data

    def run_session(self):
        if self.player_service.weekly_limit_reached():
            print(f"The weekly limit of {MAX_WEEKLY_MOBS:,} mobs has been reached.")
            return
        map_data = self.choose_map()
        if map_data is None:
            return
        encounters = 0
        print("\nContinuous exploration started. Press Ctrl+C to return to the menu between encounters.")
        try:
            while not self.player_service.weekly_limit_reached():
                encounters += 1
                self.player.turn_counter += 1
                self.player.mobs_this_week += 1
                clear_screen()
                enemy, trigger = generate_monster(
                    self.player.level,
                    map_data,
                    self.player.encounters_since_miniboss,
                    self.player.encounters_since_boss,
                )
                if enemy.rank == "Boss":
                    self.player.encounters_since_miniboss = 0
                    self.player.encounters_since_boss = 0
                elif enemy.rank == "Miniboss":
                    self.player.encounters_since_miniboss = 0
                    self.player.encounters_since_boss += 1
                else:
                    self.player.encounters_since_miniboss += 1
                    self.player.encounters_since_boss += 1
                display_name = color_text(enemy.name, RANK_COLORS.get(enemy.rank, ""))
                rank_label = color_text(enemy.rank, RANK_COLORS.get(enemy.rank, ""))
                print("\n" + "=" * 64)
                print(f"ENCOUNTER {self.player.mobs_this_week}/{MAX_WEEKLY_MOBS}")
                print(f"Enemy: [{rank_label}] {display_name}")
                print(f"Stats: HP {enemy.hp} | ATK {enemy.attack} | DEF {enemy.defense} | SPD {enemy.speed} | Dodge {enemy.dodge_chance:.0%}")
                print("=" * 64)
                if trigger != "Normal encounter":
                    print(f"  {trigger}.")
                if not self.combat_service.fight(enemy):
                    break
                print("\n--- VICTORY ---")
                print(f"Defeated: {enemy.name}")
                print(f"Rewards: {enemy.gold} gold | {enemy.exp} EXP")
                self.player.gold += enemy.gold
                self.player.exp += enemy.exp
                drops = [f"Material: {random.choice(list(self.player.materials))}"]
                potion_drop = random.random() < (0.22 if enemy.rank == "Boss" else 0.12 if enemy.rank == "Miniboss" else 0.04)
                potion_grade = "Standard"
                if enemy.rank == "Boss":
                    potion_grade = random.choice(["Superior", "Masterwork", "Transcendent"])
                elif enemy.rank == "Miniboss":
                    potion_grade = random.choice(["Greater", "Superior"])
                item_drop = None
                if potion_drop:
                    drops.append(f"{potion_grade} Healing Potion x1")
                if random.random() < (0.95 if enemy.rank == "Boss" else 0.65 if enemy.rank == "Miniboss" else 0.3):
                    item_drop = generate_item()
                    display_name = rarity_text(item_drop.name, item_drop.rarity)
                    rarity = rarity_text(item_drop.rarity, item_drop.rarity)
                    drops.append(f"{rarity} {display_name} [Power: +{item_drop.value}]")
                print("Drops:")
                for drop in drops:
                    print(f"  - {drop}")
                self.add_material_drop()
                if potion_drop:
                    self.player.add_item(healing_potion(potion_grade))
                if item_drop:
                    self.player.add_item(item_drop)
                self.combat_service.auto_heal_after_kill()
                self.player_service.level_up()
                self.save_callback()
                time.sleep(COMBAT_RESULT_DELAY)
                if enter_pressed():
                    print("Exploration ended. Returning to the adventure menu.")
                    break
        except KeyboardInterrupt:
            print("\nExploration paused. Returning to the adventure menu.")
        self.player.session_encounters = encounters
        print(f"Exploration session ended after {encounters} encounter(s).")
