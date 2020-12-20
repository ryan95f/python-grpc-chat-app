import tkinter as tk
from src.client.frame.base import BaseChatFrame


class ActiveUsersFrame(tk.Frame):
    """Frame to list the active users in the chat session"""

    __ACTIVE_USER_LIST_WIDTH = 21
    __ACTIVE_USER_LIST_HEIGHT = 18
    __ACTIVE_USER_BORDER_SIZE = 0

    def __init__(self, master):
        """ActiveUsersFrame constructor

        Args:
            master: The parent tk component. Either a frame or tkinter Tk.
        """
        super(ActiveUsersFrame, self).__init__(master)
        self.__setup_widgets()

    def __setup_widgets(self):
        self.__active_user_label = tk.Label(self, text='Active Users')
        self.__active_user_label.pack()

        self.__active_users_list = tk.Listbox(self,
                                              bd=self.__ACTIVE_USER_BORDER_SIZE,
                                              height=self.__ACTIVE_USER_LIST_HEIGHT,
                                              width=self.__ACTIVE_USER_LIST_WIDTH)
        self.__active_users_list.pack()

    def clear_active_user_list(self):
        """Clear the display list of active users"""
        messages_start_index = 0
        messsages_end_index = self.__active_users_list.size()
        self.__active_users_list.delete(messages_start_index, messsages_end_index)

    def add_active_user(self, username):
        """Add a user to the active user list display

        Args:
            username: The username to add to the list.
        """
        messages_start_index = self.__active_users_list.size() + 1
        self.__active_users_list.insert(messages_start_index, username)
