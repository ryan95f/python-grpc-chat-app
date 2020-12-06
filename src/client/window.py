import tkinter as tk
from threading import Thread
from src.client.server_utils import GrpcClient
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc

class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.title('grpc chat!')
        self.grid()
        self.__setup_widgets()
        self.client = GrpcClient()

        self.messages_to_send = []
        # self.setUpWorker()

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


    def __connect_client(self):
        username = self.username_input.get()
        result = self.client.connect(username)
        self.is_connected_msg.set('Connected')

    def __send_message(self):
        message = self.chat_box.get("1.0",'end-1c')
        self.chat_box.delete('1.0', 'end-1c')

        self.messages_to_send.append(chat_pb2.ChatMessage(userId=2, username='Ryan', message=message))
        self.__add_message('Ryan', message)

    def __add_message(self, username, message):
            self.chat_mesages.insert(self.chat_mesages.size() + 1, '[{}] - {}'.format(username, message))
        



    # def setUpWorker(self):
    #     self.t1 = Thread(target=self.__message_reciever_handler)
    #     self.t1.start()

    # def __message_reciever_handler(self):
    #     response = self.client.send_messages([chat_pb2.ChatMessage(userId=2, username='Ryan', message='Test')])
    #     for message in response:
    #         print(message)
           