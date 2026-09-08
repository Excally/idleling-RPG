from .constants import GREEN, MAX_WEEKLY_MOBS, current_week_key
from .formulas import experience_needed


class PlayerService:
    def __init__(self, player):
        self.player = player

    def reset_week_if_needed(self):
        if self.player.week_key != current_week_key():
            self.player.week_key = current_week_key()
            self.player.mobs_this_week = 0

    def weekly_limit_reached(self):
        self.reset_week_if_needed()
        return self.player.mobs_this_week >= MAX_WEEKLY_MOBS

    def level_up(self):
        while self.player.exp >= experience_needed(self.player.level):
            self.player.exp -= experience_needed(self.player.level)
            self.player.level += 1
            self.player.stats["ATK"] += 3
            self.player.max_hp += 10
            self.player.hp = self.player.max_hp
            print(f"{GREEN}Level up! You are now level {self.player.level}.{GREEN}")

    def upgrade_stat(self, choice, amount=1):
        upgrades = {"1": ("ATK", 10), "2": ("HP", 15)}
        if choice not in upgrades:
            return False, "Invalid stat choice."
        stat, cost = upgrades[choice]
        amount = max(1, amount)
        affordable_amount = self.player.gold // cost
        amount = min(amount, affordable_amount)
        if amount == 0:
            return False, f"You need {cost} gold."
        self.player.gold -= cost * amount
        if stat == "ATK":
            self.player.stats["ATK"] += amount
        else:
            self.player.max_hp += 10 * amount
            self.player.hp += 10 * amount
        return True, f"{stat} upgraded {amount} time(s). Spent {cost * amount} gold."
