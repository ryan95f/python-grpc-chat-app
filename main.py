import grpc
from src.client.window import Window
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc

from threading import Thread


def generate_messages(messages):
    for message in messages:
        yield message


def main():
    # channel = grpc.insecure_channel('localhost:50051')
    # stub = chat_pb2_grpc.ChatStub(channel)

    # messages = [chat_pb2.ChatMessage(userId=2, username='Ryan', message='Hello World')]
    # r = stub.sendMessage(generate_messages(messages))
    # for i in r:
    #     print(i)        
    
    window = Window()
    window.mainloop()


if __name__ == '__main__':
    main()
