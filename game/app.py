from .constants import CYAN, RESET
from .context import create_game_services
from .persistence import save_player


def run_game():
    services = create_game_services()
    print(f"{CYAN}=== MODULAR IDLE RPG ==={RESET}")
    try:
        services.menu.run()
    except (KeyboardInterrupt, EOFError):
        print("\nSaving progress...")
    finally:
        save_player(services.player)
        print("Progress saved. Goodbye!")
