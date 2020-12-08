import tkinter as tk
from threading import Thread
from enum import Enum

class ConnectionStatus(Enum):
    CONNECTED = 1
    DISCONNECT = 2


class ConnectionFrame(tk.Frame):
    def __init__(self, root, grpc_client):
        super(ConnectionFrame, self).__init__(root)
        self.root = root
        self.grpc_client = grpc_client

    def __setup_widgets(self):
        self.__setup_username_input_widget()
        self.__setup_connection_btn_widget()
        self.__setup_connection_status_label_widget()

    def __setup_username_input_widget(self):
        self.username_input = tk.Entry(self, width=50)
        self.username_input.grid(row=0, column=0, columnspan=3, sticky='we')

    def __setup_connection_btn_widget(self):
        self.connect_btn = tk.Button(self, width=15, command=self.__btn_action_toggle_client_connection)
        self.connect_btn.grid(row=0, column=4)

    def __btn_action_toggle_client_connection(self):
        if self.grpc_client.is_connected:
            self.__disconnect_from_server()
        else:
            self.__connect_to_server()

    def __disconnect_from_server(self):
        self.grpc_client.disconnect()
        self.is_connected_msg.set(ConnectionStatus.DISCONNECT)

    def __connect_to_server(self):
        username = self.username_input.get()
        self.user = self.grpc_client.connect(username)
        self.__set_widget_text_by_connection_status(ConnectionStatus.CONNECTED)

    def __setup_connection_status_label_widget(self):
        self.is_connected_msg = tk.StringVar()
        self.connection_status_label = tk.Label(self, width=15, textvariable=self.is_connected_msg)
        self.connection_status_label.grid(row=0, column=5)
        self.__set_widget_text_by_connection_status(ConnectionStatus.DISCONNECT)

    def __set_widget_text_by_connection_status(self, connection_status):
        connection_config_map = {
            ConnectionStatus.CONNECTED: {
                'status': 'Connected',
                'colour': 'green',
                'btn_text': 'Disconnect'
            },
            ConnectionStatus.DISCONNECT: {
                'status': 'Not Connected',
                'colour': 'red',
                'btn_text': 'Connect'
            }
        }

        current_connection_details = connection_config_map.get(connection_status.lower())
        self.is_connected_msg.set(current_connection_details['status'])
        self.connection_status_label.configure(foreground=current_connection_details['colour'])
        self.connect_btn.configure(text=current_connection_details['btn_text'])
