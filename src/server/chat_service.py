import logging
import random
import json
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc
from hashlib import md5


class ChatService(chat_pb2_grpc.ChatServicer):
    """Service to manage and distribute messages for a chat session"""

    def __init__(self):
        super(ChatService, self).__init__()
        self.chats = []
        self.users = {}
        self.stop_connection = False

    def connect(self, request, context):
        """Register a user with the chat server

        Args:
            request: A grpc ChatUser object of the user attempting
                     to connect to the server
            context: Metadata concerning the request

        Returns:
            A grpc ChatUserConnected object with thier requested
            username and a randomly generated user id
        """
        user_id = random.randint(1, 10000)
        self.users[user_id] = request.username
        logging.info(f'User {user_id} has connected')
        return chat_pb2.ChatUserConnected(username=request.username, userId=user_id)

    def disconnect(self, request, context):
        """De-register a user from the chat server

        Args:
            request: A grpc ChatUserConnected object for the disconnecting user
            context: Metadata concerning the request

        Returns:
            A grpc ChatUserDisconnect object with the
            isDisconnected property set to true
        """
        del self.users[request.userId]
        logging.info(f'User {request.userId} has disconnected')
        return chat_pb2.ChatUserDisconnect(isDisconnected=True)

    def sendMessage(self, request, context):
        """Endpoint to recieve a message from the client

        Args:
            request: A grpc ChatMessage object containing the
                     message and user information
            context: Metadata concerning the request

        Returns:
            A grpc ChatMessage object with the user Id
            and username from the user who send the message
        """
        logging.info(f'User {request.userId} has sent a message')
        self.chats.append(request)
        return chat_pb2.ChatMessage(userId=request.userId, username=request.username, message=request.message)

    def subscribeMessages(self, request, context):
        """Endpoint to subscribe to new messages from different users on the chat server.

        Args:
            request: A grpc ChatUserConnected object of the subscribing user
            context: Metadata concerning the request

        Returns:
            A stream of grpc ChatMessage objects from other users on the server
        """
        current_user_id = request.userId
        last_seen_message_index = 0

        logging.info(f'User {request.userId} has subscribed to incoming messages')
        while not self.stop_connection and self.__is_user_still_connected(current_user_id):
            while len(self.chats) > last_seen_message_index:
                message = self.chats[last_seen_message_index]
                last_seen_message_index += 1
                if message.userId != current_user_id:
                    yield message

    def __is_user_still_connected(self, user_id):
        return self.users.get(user_id, None) is not None

    def subscribeActiveUsers(self, request, context):
        """Endpoint to subscribe to active users on the chat server

        Args:
            request: A grpc ChatUserConnected object of the subscribing user
            context: Metadata concerning the request

        Returns:
            A streaam of grpc ChatActiveUser objects
        """
        current_hash = ""
        current_user_id = request.userId

        logging.info(f'User {request.userId} has subscribed to active users')

        while not self.stop_connection and self.__is_user_still_connected(current_user_id):
            json_users = json.dumps(self.users)
            md5_hash = md5(bytes(json_users, 'utf-8')).hexdigest()
            if current_hash != md5_hash:
                current_hash = md5_hash
                for user_id, username in self.users.items():
                    if user_id != current_user_id:
                        yield chat_pb2.ChatActiveUser(username=username,
                                                      userId=user_id,
                                                      currentHash=current_hash)
