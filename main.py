import grpc
import tkinter as tk
from src.client.window import Window
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc

def main():
    # channel = grpc.insecure_channel('localhost:50051')
    # stub = chat_pb2_grpc.ChatStub(channel)
    # r = stub.connect(chat_pb2.ChatUser(username='Ryan'))
    
    # root = tk.Tk()
    window = Window()
    window.mainloop()


if __name__ == '__main__':
    main()
