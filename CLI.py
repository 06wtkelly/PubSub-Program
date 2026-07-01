class ClientCLI:

    def display_error(self, message: str) -> None:
        print(f"[ERROR] {message}")

    def display_successful_command(self, message: str) -> None:
        print(f"[SUCCESS] {message}")
