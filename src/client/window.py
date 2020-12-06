import tkinter as tk
from src.client.server_utils import GrpcClient

class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.title('grpc chat!')
        self.grid()
        self.__setup_widgets()
        self.client = GrpcClient()

    def __setup_widgets(self):
        self.username_input = tk.Entry(self, width=50)
        self.username_input.grid(row=0, column=0, columnspan=3)

        self.connect_btn = tk.Button(self, text='Connect', width=15, command=self.__connect_client)
        self.connect_btn.grid(row=0, column=4)

        self.is_connected_msg = tk.StringVar(value='Not Connected')
        self.connection_status_label = tk.Label(self, width=15, textvariable=self.is_connected_msg)
        self.connection_status_label.grid(row=0, column=5)

        self.chat_mesages = tk.Label(self, height=20)
        self.chat_mesages.grid(row=1, column=0, columnspan=3)

        self.chat_box = tk.Text(self, height=5)
        self.chat_box.grid(row=2, column=0, columnspan=3)

        self.send_btn = tk.Button(self, text='Send', height=5, width=20)
        self.send_btn.grid(row=2, column=5)


    def __connect_client(self):
        username = self.username_input.get()
        result = self.client.connect(username)
        self.is_connected_msg.set('Connected')
