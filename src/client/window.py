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
        self.text_input = tk.Entry(self)
        self.text_input.grid(column=0, row=0, columnspan=3)

        self.connect_btn = tk.Button(self, text='Connect', command=self.__connect_client)
        self.connect_btn.grid(row=0, column=5)

    def __connect_client(self):
        username = self.text_input.get()
        result = self.client.connect(username)
        print(result)