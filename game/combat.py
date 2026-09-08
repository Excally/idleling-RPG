import random
import time

from .constants import BLUE, COMBAT_ACTION_DELAY, GOLD, RED, RANDOM_POTION_CHANCE, RESET
from .formulas import roll_damage


class CombatService:
    def __init__(self, player):
        self.player = player

    def maybe_use_potion(self, reason):
        player = self.player
        if player.hp >= player.max_hp or random.random() >= RANDOM_POTION_CHANCE:
            return False
        potion = player.strongest_item("Healing Potion")
        if not potion:
            return False
        old_hp = player.hp
        player.remove_one_item(potion)
        player.heal(potion.value)
        print(f"{GOLD}{potion.name} automatically used ({reason}): {old_hp} -> {player.hp} HP.{RESET}")
        return True

    def auto_heal_after_kill(self):
        player = self.player
        if player.hp > player.max_hp * 0.6:
            return False
        potion = player.strongest_item("Healing Potion")
        if not potion:
            return False
        player.remove_one_item(potion)
        old_hp = player.hp
        player.heal(potion.value)
        print(f"{GOLD}{potion.name} used after the kill: {old_hp} -> {player.hp} HP.{RESET}")
        return True

    def _passive_modifiers(self):
        attack_multiplier = 1.0
        defense_multiplier = 1.0
        for skill in self.player.skills:
            if not skill.passive:
                continue
            if skill.buff_type == "passive_attack":
                attack_multiplier += skill.buff_value
            elif skill.buff_type == "passive_defense":
                defense_multiplier += skill.buff_value
        return attack_multiplier, defense_multiplier

    def _player_attack(self, enemy, skill):
        player = self.player
        attack_multiplier, _ = self._passive_modifiers()
        damage, critical = roll_damage(
            int(player.total_attack() * attack_multiplier),
            player.stats["CRIT_CHANCE"] + (0.08 if player.has_enchantment("Focused") else 0),
            player.stats["CRIT_DMG"],
        )
        triggered_skill = skill if random.random() < skill.proc_chance else None
        final_damage = max(1, int(damage * (triggered_skill.damage_multiplier if triggered_skill else 1.0)))
        enemy.hp -= final_damage
        if triggered_skill:
            print(f"   {BLUE}{triggered_skill.effect_text} for {final_damage} damage!{RESET}")
            if triggered_skill.buff_type == "lifesteal":
                player.heal(int(final_damage * triggered_skill.buff_value))
            if triggered_skill.buff_type == "damage_over_time":
                enemy.hp -= int(enemy.hp * triggered_skill.buff_value)
            if triggered_skill.buff_type == "stun":
                return True
        else:
            marker = f"{GOLD}CRITICAL!{RESET}" if critical else "Attack"
            print(f"   {marker} You deal {final_damage} damage.")
        return False

    def fight(self, enemy):
        player = self.player
        skill = next((skill for skill in player.skills if not skill.passive), player.skills[0])
        player_turn = player.total_speed() >= enemy.speed
        print(f"Speed order: {'Player' if player_turn else enemy.name} acts first.")
        while enemy.hp > 0 and player.hp > 0:
            if player_turn:
                stunned = self._player_attack(enemy, skill)
                time.sleep(COMBAT_ACTION_DELAY)
                self.maybe_use_potion("after an action")
                if enemy.hp <= 0:
                    break
                if player.has_enchantment("Double Strike") and random.random() < 0.2:
                    print("   Enchantment triggered: second attack.")
                    self._player_attack(enemy, skill)
                    time.sleep(COMBAT_ACTION_DELAY)
                    if enemy.hp <= 0:
                        break
                if stunned:
                    print(f"   {enemy.name} is stunned and loses its turn.")
                    player_turn = True
                    continue
            else:
                print(f"   {RED}{enemy.name} acts first.{RESET}")
            _, defense_multiplier = self._passive_modifiers()
            incoming = max(1, int(enemy.attack - player.total_defense() * defense_multiplier))
            if player.has_enchantment("Bulwark"):
                incoming = max(1, int(incoming * 0.85))
            player.hp -= incoming
            print(f"   {RED}{enemy.name} hits for {incoming} damage!{RESET} HP: {max(player.hp, 0)}/{player.max_hp}")
            time.sleep(COMBAT_ACTION_DELAY)
            self.maybe_use_potion("after taking damage")
            if player.hp <= 0:
                print("\n=== DEFEAT ===")
                print(f"You were defeated by {enemy.name}.")
                input("Press Enter to confirm and return to the adventure menu: ")
                player.hp = player.max_hp
                return False
            player_turn = True
        return True
