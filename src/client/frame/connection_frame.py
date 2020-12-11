import tkinter as tk
from threading import Thread
from enum import Enum

from src.client.frame.base import BaseChatFrame


class ConnectionStatus(Enum):
    CONNECTED = 1
    DISCONNECT = 2


class ConnectionFrame(BaseChatFrame):
    """Frame to enable a user to connect or disconnect from the chat server"""

    __BUTTON_WIDTH = 15
    __STATUS_LABLE_WIDTH = 15

    def __init__(self, master, grpc_client, connected_callback=None, disconnect_callback=None):
        """ConnectionFrame constructor

        Args:
            master:                 The parent tk component. Either a frame or tkinter Tk.
            grpc_client:            The grpc client wrapper to communicate with the server.
            connected_callback:     Callback that is executed once the user has connected to the server
            disconnect_callback:    Callback that is executed once the user has disconnected from the server
        """
        super(ConnectionFrame, self).__init__(master, grpc_client)
        self._connected_callback = connected_callback
        self._disconnect_callback = disconnect_callback

        self.__connection_config_map = {
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

        self.__setup_widgets()

    def __del__(self):
        if self._grpc_client.is_connected:
            self.__disconnect_from_server()

    def __setup_widgets(self):
        self.__setup_username_input_widget()
        self.__setup_connection_btn_widget()
        self.__setup_connection_status_label_widget()

    def __setup_username_input_widget(self):
        self.username_input = tk.Entry(self)
        self.username_input.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def __setup_connection_btn_widget(self):
        self.connect_btn = tk.Button(self, width=self.__BUTTON_WIDTH, command=self.__btn_action_toggle_client_connection)
        self.connect_btn.pack(side=tk.LEFT)

    def __btn_action_toggle_client_connection(self):
        if self._grpc_client.is_connected:
            self.__disconnect_from_server()
        else:
            self.__connect_to_server()

    def __disconnect_from_server(self):
        self._grpc_client.disconnect()
        self.__set_widget_text_by_connection_status(ConnectionStatus.DISCONNECT)
        if self._disconnect_callback is not None:
            self._disconnect_callback()

    def __connect_to_server(self):
        username = self.username_input.get()
        self.user = self._grpc_client.connect(username)
        self.__set_widget_text_by_connection_status(ConnectionStatus.CONNECTED)

        if self._connected_callback is not None:
            self._connected_callback()

    def __setup_connection_status_label_widget(self):
        self.is_connected_msg = tk.StringVar()
        self.connection_status_label = tk.Label(self, width=self.__STATUS_LABLE_WIDTH, textvariable=self.is_connected_msg)
        self.connection_status_label.pack(side=tk.LEFT)
        self.__set_widget_text_by_connection_status(ConnectionStatus.DISCONNECT)

    def __set_widget_text_by_connection_status(self, connection_status):
        current_connection_details = self.__connection_config_map.get(connection_status)
        self.is_connected_msg.set(current_connection_details['status'])
        self.connection_status_label.configure(foreground=current_connection_details['colour'])
        self.connect_btn.configure(text=current_connection_details['btn_text'])
