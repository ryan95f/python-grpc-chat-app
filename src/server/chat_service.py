import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc

class ChatService(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        super(ChatService, self).__init__()
        self.chats = []

    def connect(self, request, context):
        print(request)
        return chat_pb2.ChatUserConnected(username=request.username, userId=1)
