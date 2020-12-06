import grpc
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc

class GrpcClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = chat_pb2_grpc.ChatStub(self.channel)
        self.__is_connected = False
        self.user = None

    @property
    def is_connected(self):
        return self.__is_connected

    def connect(self, username):
        response = self.stub.connect(chat_pb2.ChatUser(username=username))
        self.user = response
        self.__is_connected = True
        return response

    def disconnect(self):
        response = self.stub.disconnect(self.user)
        self.user = None
        self.__is_connected = False
        return True

    def subscribe_messages(self):
        return self.stub.subscribeMessages(self.user)

    def send_message(self, message):
        return self.stub.sendMessage(message)