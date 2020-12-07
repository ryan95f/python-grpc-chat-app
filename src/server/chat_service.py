import random
import json
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc
from hashlib import md5

class ChatService(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        super(ChatService, self).__init__()
        self.chats = []
        self.users = {}
        self.stop_connection = False

    def connect(self, request, context):
        user_id = random.randint(1, 10000)
        user = chat_pb2.ChatUserConnected(username=request.username, userId=user_id)
        self.users[user_id] = user
        return user

    def disconnect(self, request, context):
        del self.users[request.userId]
        return chat_pb2.ChatUserDisconnect(isDisconnected=True)

    def sendMessage(self, request, context):
        self.chats.append(request)
        return chat_pb2.ChatMessage(userId=request.userId, username=request.username)

    def subscribeMessages(self, request, context):
        current_user_id = request.userId
        last_seen_message_index = 0

        while not self.stop_connection and self.__is_user_still_connected(current_user_id):
            while len(self.chats) > last_seen_message_index:
                message = self.chats[last_seen_message_index]
                last_seen_message_index += 1
                if message.userId != current_user_id:
                    yield message

    def __is_user_still_connected(self, user_id):
        return self.users.get(user_id, None) != None

    def subscribeActiveUsers(self, request, context):
        current_hash = ""
        current_user_id = request.userId
        
        while not self.stop_connection and self.__is_user_still_connected(current_user_id):
            json = json.dumps(self.users)
            md5_hash = md5(json).hexdigest()
            if current_hash != md5_hash:
                current_hash = md5_hash
                for user in self.users:
                    if user.userId != current_user_id:
                        yield user
