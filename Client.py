from threading import Thread
import select
import sys

from Subscriptions import SubscriptionManager
from CommandHandler import ClientCommandHandler
from FileHandler import FileHandler
from RateLimiter import RateLimiter
from TerminalInterface import ClientCLI

class Client:
    """___"""

    def __init__(self, client_id, connection):
        """ Initialise Client with the client_id and connection.
            
        Parameters:
            - client_id (str): the identifier of the Client
            - connection (__): the connection to a connected server
        """
        self.identifier = client_id
        self.connection = connection

        self.subscriptions = SubscriptionManager()
        self.rate_limiter = RateLimiter()
        self.file_handler = FileHandler()
        self.commands = ClientCommandHandler(self)
        self.interface = ClientCLI()

        self._running = False
        self._error_code = 0

    def subscribe(self, topic, filter_criteria) -> bool:
        """Subscribes the client to the given topic. Optionally gives the
        subscription a numerical operator and value.

        Parameters:
            - topic (str): the topic to subscribe to
            - filter_criteria (str | None): the filter criteria in the form of [topic, filter] or None

        Throws:
            - DuplicateSubscriptionException
            - InvalidSubscriptionFilterException

        Returns True if a subscription was successful, otherwise throws an exception
        """
        return self.subscriptions.add_subscription(topic, filter_criteria)

    def unsubscribe(self, topic) -> bool:
        """Unsubscribes the client from all subscriptions with the given topic.
        
        Parameters:
            - topic (str): the topic to unsubscribe from

        Returns:
            - True if successfully unsubscribed from given topic
            - False if the client has no subscriptions of the given topic
        """
        return self.subscriptions.remove_subscription(topic)

    def quit(self) -> None:
        """Makes the client quit from reading user input and receiving information."""
        self._running = False
        self._error_code = 0

    def read_user_input(self):
        """ Reads user input from stdin.

        Returns the read string from stdin

        Warnings:
            - Possible errors on Windows systems due to use of select library
            - If EOFError or KeyboardInterrupt is triggered, the client will quit with an error code
        """
        try:
            ready, _, _ = select.select([sys.stdin], [], [], 0.2)
            if ready:
                return sys.stdin.readline().strip()
        except (EOFError, KeyboardInterrupt) as e:
            print(f"[DEBUG] Exception in read_user_input, exiting...")
            self._running = False
            self._error_code = 1
            return ""

    def handle_user_input(self, args: str):
        """Handles the given argument from user, processes and runs
        the proper functionality.

        Parameters:
            - args (str): the string input from a client user

        Returns True if a command was successfuly executed
        """
        cmd, cmd_args = self.commands.parse_command(args)
        if not cmd and not cmd_args:
            return True

        self.commands.handle_command(cmd, cmd_args)

    def receive_from_server(self):
        pass

    def read_server_message(self):
        pass

    def handle_server_message(self):
        pass

    def run(self):
        """Runs the Client, staring reading user input and receiving messages
        from the connected server program.

        Returns the current error code of the Client. 0 if OK, otherwise Error
        """
        self._running = True

        Thread(
            target=self.receive_from_server,
            args=(),
            daemon=True
        ).start()

        while self._running:
            user_input = self.read_user_input()
            if not user_input:
                continue    # Nothing to process so just loop again

            # print(f"[ECHO] {user_input}")

            self.handle_user_input(user_input)
            if self._error_code != 0:
                break

        print(f"exiting with code: {self._error_code}")
        return self._error_code
