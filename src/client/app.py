import tkinter as tk
from threading import Thread
import src.client.chat_client as client

import src.client.frame as frame
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc


class ChatApp(tk.Tk):
    """Tkinter Chat application to send messages to other users"""

    def __init__(self):
        super(ChatApp, self).__init__()
        self.title('Chat Application with gRPC!')
        self.grid()
        self.resizable(False, False)

        self.__reciever_thread = None
        self.__active_user_thread = None
        self.__client = client.ChatClient()
        self.__setup_widgets()

    def __del__(self):
        if self.__reciever_thread is not None:
            self.__reciever_thread.join()

        if self.__active_user_thread is not None:
            self.__active_user_thread.join()

    def __setup_widgets(self):
        self.connection_frame = frame.ConnectionFrame(self, self.__client,
                                                      connected_callback=self.__connected_callback,
                                                      disconnect_callback=self.__disconnected_callback)
        self.connection_frame.grid(row=0, column=0, columnspan=5, sticky=tk.EW)

        self.__chat_message_frame = frame.ChatMessagesFrame(self)
        self.__chat_message_frame.grid(row=1, column=0, columnspan=4, sticky=tk.EW)

        self.__active_user_frame = frame.ActiveUsersFrame(self)
        self.__active_user_frame.grid(row=1, column=4, columnspan=2)

        self.__chatbox_frame = frame.ChatboxFrame(self, self.__client, message_send_callback=self.__message_send_callback)
        self.__chatbox_frame.grid(row=2, column=0, columnspan=5, sticky=tk.EW)

        self.protocol("WM_DELETE_WINDOW", self.__on_close)

    def __on_close(self):
        if self.__client.is_connected:
            self.__client.disconnect()
        self.destroy()

    def __connected_callback(self):
        self.__chatbox_frame.enable_send_btn()

        self.__reciever_thread = Thread(target=self.__message_reciever_handler)
        self.__reciever_thread.start()

        self.__active_user_thread = Thread(target=self.__active_user_reciever_handler)
        self.__active_user_thread.start()

    def __message_reciever_handler(self):
        response = self.__client.subscribe_messages()
        for message in response:
            self.__chat_message_frame.add_message(message.username, message.message)

    def __active_user_reciever_handler(self):
        response = self.__client.subscribe_active_users()
        current_hash = ""
        for user in response:
            if current_hash != user.currentHash:
                current_hash = user.currentHash
                self.__active_user_frame.clear_active_user_list()
            self.__active_user_frame.add_active_user(user.username)

    def __disconnected_callback(self):
        self.__chatbox_frame.disable_send_btn()
        self.__chat_message_frame.clear_chat_messages()
        self.__active_user_frame.clear_active_user_list()

    def __message_send_callback(self, msg):
        self.__chat_message_frame.add_message(self.__client.username, msg)
