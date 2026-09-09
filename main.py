try:
    from game.app import run_game
except ModuleNotFoundError as e:
    print(f"\n[!] Missing dependency: {e.name}")
    print("    Run this first (only once):")
    print("\n        pip install -r requirements.txt\n")
    raise SystemExit(1)


if __name__ == "__main__":
    run_game()
