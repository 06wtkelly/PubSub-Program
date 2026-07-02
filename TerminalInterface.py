class ClientCLI:

    def display_error(self, message: str) -> None:
        print(f"[ERROR] {message}")

    def display_successful_command(self, message: str) -> None:
        print(f"[SUCCESS] {message}")

    def display_all_subscriptions(self, subscriptions) -> None:
        for sub in subscriptions:
            print(sub)
