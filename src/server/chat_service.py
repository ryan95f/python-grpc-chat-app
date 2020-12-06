from threading import Thread
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc

class ChatService(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        super(ChatService, self).__init__()
        self.chats = []
        self.users = {}
        self.stop_thread = False

    def connect(self, request, context):
        return chat_pb2.ChatUserConnected(username=request.username, userId=1)

    def disconnect(self, request, context):
        return chat_pb2.ChatUserConnected(isDisconnected=True)

    def sendMessage(self, request_iterator, context):
        current_user_id = 0
        last_seen_message_index = 0

        for incoming_chats in request_iterator:
            print(incoming_chats)
            current_user_id = incoming_chats.userId
            self.chats.append(incoming_chats)

        while not self.stop_thread:
            while len(self.chats) > last_seen_message_index:
                message = self.chats[last_seen_message_index]
                last_seen_message_index += 1
                if message.userId != current_user_id:
                    print(message)
                    yield message
