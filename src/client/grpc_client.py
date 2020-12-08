import grpc
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc

class GrpcClient:
    def __init__(self):
        self.__channel = grpc.insecure_channel('localhost:50051')
        self.__stub = chat_pb2_grpc.ChatStub(self.__channel)
        self.__user = None
        self.__is_connected = False

    @property
    def is_connected(self):
        return self.__is_connected

    @property
    def username(self):
        return self.__user.username

    def connect(self, username):
        response = self.__stub.connect(chat_pb2.ChatUser(username=username))
        self.__user = response
        self.__is_connected = True
        return response

    def disconnect(self):
        self.__stub.disconnect(self.__user)
        self.__user = None
        self.__is_connected = False
        return True

    def subscribe_messages(self):
        return self.__stub.subscribeMessages(self.__user)

    def send_message(self, message):
        return self.__stub.sendMessage(message)

    def subscribe_active_users(self):
        return self.__stub.subscribeActiveUsers(self.__user)