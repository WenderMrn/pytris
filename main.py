from core import game


if __name__ == "__main__":
    try:
        game.run()
    except KeyboardInterrupt:
        # print("\nExecution interrupted by the user.")
        pass
