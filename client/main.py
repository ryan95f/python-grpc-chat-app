import grpc
import server.chat_pb2 as chat_pb2
import server.chat_pb2_grpc as chat_pb2_grpc

USERNAME = 'Ryan'

def create_user(username):
    return chat_pb2.ChatUser(username=username)

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = chat_pb2_grpc.ChatStub(channel)
    user = create_user(USERNAME)
    r = stub.connect(user)
    print(r)

if __name__ == '__main__':
    main()
