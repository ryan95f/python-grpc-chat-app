import grpc
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc

class GrpcClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = chat_pb2_grpc.ChatStub(self.channel)
        self.is_connected = False

    def connect(self, username):
        r = self.stub.connect(chat_pb2.ChatUser(username=username))
        self.is_connected = True
        return r

    def send_messages(self, messages):
        print(messages)
        return self.stub.sendMessage(self.__messages_to_iter(messages))

    def __messages_to_iter(self, messages):
        for message in messages:
            yield message
