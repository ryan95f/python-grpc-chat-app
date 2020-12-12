import tkinter as tk


class ChatMessagesFrame(tk.Frame):
    """A tkinter frame to display chat messages for the current chat session"""

    __CHAT_MESSAGE_HEIGHT = 20

    def __init__(self, master):
        """ChatMessagesFrame constructor

        Args:
            master: The parent tk component. Either a frame or tkinter Tk
        """
        super(ChatMessagesFrame, self).__init__(master)
        self.__setup_chat_messages_widget()

    def __setup_chat_messages_widget(self):
        self.__chat_messages = tk.Listbox(self, height=self.__CHAT_MESSAGE_HEIGHT)
        self.__chat_messages.pack(fill=tk.BOTH)

    def add_message(self, username, message):
        """Add a user's message to the chatbox

        Args:
            message: The user's message
            username: The user's username
        """
        next_item_index = self.__chat_messages.size() + 1
        self.__chat_messages.insert(next_item_index, '[{:10}] - {}'.format(username, message))

    def clear_chat_messages(self):
        """Clear the current session chat messages"""
        messages_start_index = 0
        messsages_end_index = self.__chat_messages.size()
        self.__chat_messages.delete(messages_start_index, messsages_end_index)
