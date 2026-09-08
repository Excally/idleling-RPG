from dataclasses import dataclass
from typing import Callable

from .combat import CombatService
from .constants import clear_screen
from .crafting import CraftingService
from .exploration import ExplorationService
from .inventory import InventoryService
from .menus import MenuService
from .persistence import load_player, save_player
from .player import PlayerService
from .shop import ShopService


@dataclass
class GameServices:
    player: object
    player_service: PlayerService
    inventory: InventoryService
    combat: CombatService
    shop: ShopService
    crafting: CraftingService
    exploration: ExplorationService
    menu: MenuService


def create_game_services() -> GameServices:
    player = load_player()
    player_service = PlayerService(player)
    inventory = InventoryService(player, clear_screen)
    combat = CombatService(player)
    shop = ShopService(player)
    crafting = CraftingService(player)
    save: Callable[[], None] = lambda: save_player(player)
    exploration = ExplorationService(player, player_service, combat, save)
    menu = MenuService(player, player_service, inventory, shop, crafting, exploration)
    return GameServices(player, player_service, inventory, combat, shop, crafting, exploration, menu)
