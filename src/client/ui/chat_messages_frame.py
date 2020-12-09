import tkinter as tk
from src.client.ui.base import BaseChatFrame

class ChatMessagesFrame(BaseChatFrame):
    def __init__(self, master, grpc_client):
        super(ChatMessagesFrame, self).__init__(master, grpc_client)
        self.__setup_chat_messages_widget()
    
    def __setup_chat_messages_widget(self):
        self.chat_mesages = tk.Listbox(self, height=20)
        self.chat_mesages.pack(fill=tk.BOTH)

    def add_message(self, message):
        username = self.grpc_client.username
        self.chat_mesages.insert(self.chat_mesages.size() + 1, '[{:10}] - {}'.format(username, message))

    def add_incoming_message(self, message, username):
        self.chat_mesages.insert(self.chat_mesages.size() + 1, '[{:10}] - {}'.format(username, message))

    def clear_chat_messages(self):
        messages_start_index = 0
        messsages_end_index = self.chat_mesages.size()
        self.chat_mesages.delete(messages_start_index, messsages_end_index)
