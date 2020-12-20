import grpc
import src.utils as utils
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc
import src.client.exceptions as client_exceptions

YAML_CONFIG_PATH = './config.yaml'


class ChatClient:
    """Wrapper class to interact with the grpc chat server"""

    def __init__(self):
        server_host, server_port = self.__get_server_config_from_file()
        self.__channel = grpc.insecure_channel(f'{server_host}:{server_port}')
        self.__stub = chat_pb2_grpc.ChatStub(self.__channel)
        self.__user = None
        self.__is_connected = False

    def __get_server_config_from_file(self):
        yaml_config = utils.read_yaml_config(YAML_CONFIG_PATH)
        return utils.get_server_config_from_yaml(yaml_config)

    @property
    def is_connected(self):
        return self.__is_connected

    @property
    def username(self):
        if not self.__is_connected:
            return None
        return self.__user.username

    @property
    def user_id(self):
        if not self.__is_connected:
            return -1
        return self.__user.userId

    def connect(self, username):
        """Connect to the chat server

        Args:
            username: The username to register against the chat server
        """
        response = self.__stub.connect(chat_pb2.ChatUser(username=username))
        self.__user = response
        self.__is_connected = True
        return response

    def disconnect(self):
        """Disconnect from the chat server

        Returns:
            boolean: True to indicate the disconnection was successful.
        """
        if not self.is_connected:
            return True

        self.__stub.disconnect(self.__user)
        self.__user = None
        self.__is_connected = False
        return True

    def subscribe_messages(self):
        """Subscribe against the chat server to recieve new messages

        Raises:
            NotConnectedError: Raised when a connection has not been made to the chat server.
        """
        if not self.__is_connected:
            raise client_exceptions.NotConnectedError("Error: you have not connected to the chat server!")

        return self.__stub.subscribeMessages(self.__user)

    def send_message(self, message):
        """Send a message to the chat server

        Raises:
            NotConnectedError: Raised when a connection has not been made to the chat server.
        """
        if not self.__is_connected:
            raise client_exceptions.NotConnectedError("Error: you have not connected to the chat server!")
        return self.__stub.sendMessage(message)

    def subscribe_active_users(self):
        """Subscribe against the chat server to recieve the active users

        Raises:
            NotConnectedError: Raised when a connection has not been made to the chat server.
        """
        if not self.__is_connected:
            raise client_exceptions.NotConnectedError("Error: you have not connected to the chat server!")
        return self.__stub.subscribeActiveUsers(self.__user)
