import tkinter as tk
from threading import Thread
from src.client.grpc_client import GrpcClient

import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc


class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.title('grpc chat!')
        self.grid()
        self.client = GrpcClient()
        self.__setup_widgets()

    def __del__(self):
        if self.client.is_connected:
            self.client.disconnect()

    def __setup_widgets(self):
        self.username_input = tk.Entry(self, width=50)
        self.username_input.grid(row=0, column=0, columnspan=3, sticky='we')

        self.connect_btn = tk.Button(self, text='Connect', width=15, command=self.__connect_client)
        self.connect_btn.grid(row=0, column=4)

        self.is_connected_msg = tk.StringVar(value='Not Connected')
        self.connection_status_label = tk.Label(self, width=15, textvariable=self.is_connected_msg)
        self.connection_status_label.grid(row=0, column=5)

        self.chat_messages_var = tk.StringVar()
        self.chat_mesages = tk.Listbox(self, height=20)
        self.chat_mesages.grid(row=1, column=0, columnspan=3, sticky='we')

        self.chat_box = tk.Text(self, height=5)
        self.chat_box.grid(row=2, column=0, columnspan=3)

        self.send_btn = tk.Button(self, text='Send', height=5, width=20, command=self.__send_message)
        self.send_btn.grid(row=2, column=4, columnspan=2, sticky='we')

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        if self.client.is_connected:
            self.client.disconnect()
        self.destroy()

    def __connect_client(self):
        if self.client.is_connected:
            self.client.disconnect()
            self.is_connected_msg.set('Not Connected')
        else:
            username = self.username_input.get()
            self.user = self.client.connect(username)
            self.is_connected_msg.set('Connected')
            self.t1 = Thread(target=self.__message_reciever_handler, args=(self.client, ))
            self.t1.start()

    def __send_message(self):
        message = self.chat_box.get("1.0",'end-1c')
        self.chat_box.delete('1.0', 'end-1c')

        message_to_send = chat_pb2.ChatMessage(
            userId=self.user.userId,
            username=self.user.username,
            message=message
        )
        self.client.send_message(message_to_send)
        self.__add_message(self.user.username, message)

    def __add_message(self, username, message):
            self.chat_mesages.insert(self.chat_mesages.size() + 1, '[{}] - {}'.format(username, message))

    def __message_reciever_handler(self, client):
        response = client.subscribe_messages()
        for message in response:
            self.__add_message(message.username, message.message)
