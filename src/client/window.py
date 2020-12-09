import tkinter as tk
from threading import Thread
from src.client.grpc_client import GrpcClient

import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc
from src.client.ui import ConnectionFrame, ChatboxFrame, ChatMessagesFrame


class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.title('grpc chat!')
        self.grid()
        self.resizable(False, False)

        self.__client = GrpcClient()
        self.__setup_widgets()

    def __del__(self):
        if self.__client.is_connected:
            self.__client.disconnect()
        self.__reciever_thread.join()
        self.__active_user_thread.join()

    def __setup_widgets(self):
        self.connection_frame = ConnectionFrame(self, self.__client)
        self.connection_frame.grid(row=0, column=0, columnspan=5, sticky='we')

        self.chat_message_frame = ChatMessagesFrame(self, self.__client)
        self.chat_message_frame.grid(row=1, column=0, columnspan=5, sticky='we')

        self.chatbox_frame = ChatboxFrame(self, self.__client)
        self.chatbox_frame.grid(row=2, column=0, columnspan=5, sticky='we')
        
        # self.username_input = tk.Entry(self, width=50)
        # self.username_input.grid(row=0, column=0, columnspan=3, sticky='we')

        # self.connect_btn = tk.Button(self, text='Connect', width=15, command=self.__btn_action_toggle_client_connection)
        # self.connect_btn.grid(row=0, column=4)

        # self.is_connected_msg = tk.StringVar(value='Not Connected')
        # self.connection_status_label = tk.Label(self, width=15, foreground='red', textvariable=self.is_connected_msg)
        # self.connection_status_label.grid(row=0, column=5)

        # self.chat_mesages = tk.Listbox(self, height=20)
        # self.chat_mesages.grid(row=1, column=0, columnspan=3, sticky='we')

        # self.chat_box = tk.Text(self, height=5)
        # self.chat_box.grid(row=2, column=0, columnspan=3)

        # self.send_btn = tk.Button(self, text='Send', height=5, width=20, command=self.__btn_action_send_message)
        # self.send_btn.grid(row=2, column=4, columnspan=2, sticky='we')
        # self.send_btn['state'] = 'disabled'

        

        self.protocol("WM_DELETE_WINDOW", self.__on_close)

        # self.active_users_list = tk.Listbox(self, height=10)
        # self.active_users_list.grid(row=1, column=4, columnspan=2, sticky='we')

    # def __btn_action_toggle_client_connection(self):
    #     if self.__client.is_connected:
    #         self.__disconnect_from_server()
    #         self.__clear_chat_messages()
    #         self.__clear_active_user_list()
    #     else:
    #         self.__connect_to_server()

    # def __disconnect_from_server(self):
    #     self.__client.disconnect()
    #     self.is_connected_msg.set('Not Connected')
    #     self.connection_status_label.configure(foreground='red')
    #     self.connect_btn.configure(text='Connect')
    #     self.send_btn['state'] = 'disabled'

    # def __connect_to_server(self):
    #     username = self.username_input.get()
    #     self.user = self.__client.connect(username)
    #     self.is_connected_msg.set('Connected')
    #     self.send_btn['state'] = 'active'
    #     self.connection_status_label.configure(foreground='green')
    #     self.connect_btn.configure(text='Disconnect')

    #     self.__reciever_thread = Thread(target=self.__message_reciever_handler)
    #     self.__reciever_thread.start()
        
    #     self.__active_user_thread = Thread(target=self.__active_user_reciever_handler)
    #     self.__active_user_thread.start()

    # def __message_reciever_handler(self):
    #     response = self.__client.subscribe_messages()
    #     for message in response:
    #         self.__display_chat_message(message.username, message.message)

    # def __display_chat_message(self, username, message):
    #         self.chat_mesages.insert(self.chat_mesages.size() + 1, '[{:10}] - {}'.format(username, message))

    # def __active_user_reciever_handler(self):
    #     response = self.__client.subscribe_active_users()
    #     messages_start_index = 1
    #     current_hash = ""
    #     for user in response:
    #         if current_hash != user.currentHash:
    #             current_hash = user.currentHash
    #             self.__clear_active_user_list()
    #             messages_start_index = 1
    #         self.active_users_list.insert(messages_start_index, user.username)
    #         messages_start_index += 1

    # def __btn_action_send_message(self):
    #     message = self.__get_users_message()
    #     self.__clear_users_message_box()

    #     grpc_message = self.__construct_message_payload(message)

    #     self.__display_chat_message(self.user.username, message)
    #     self.__client.send_message(grpc_message)

    # def __get_users_message(self):
    #     return self.chat_box.get('1.0','end-1c')
        
    # def __clear_users_message_box(self):
    #     self.chat_box.delete('1.0', 'end-1c')

    # def __construct_message_payload(self, message):
    #     return chat_pb2.ChatMessage(
    #         userId=self.user.userId,
    #         username=self.user.username,
    #         message=message
    #     )

    def __on_close(self):
        if self.__client.is_connected:
            self.__client.disconnect()
        self.destroy()

    # def __clear_chat_messages(self):
    #     messages_start_index = 0
    #     messsages_end_index = self.chat_mesages.size()
    #     self.chat_mesages.delete(messages_start_index, messsages_end_index)

    # def __clear_active_user_list(self):
    #     messages_start_index = 0
    #     messsages_end_index = self.active_users_list.size()
    #     self.active_users_list.delete(messages_start_index, messsages_end_index)