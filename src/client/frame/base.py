import tkinter as tk


class BaseChatFrame(tk.Frame):
    """Base class for a frame that requires access to the grpc client"""

    def __init__(self, master, grpc_client):
        """BaseChatFrame Constructor

        Args:
            master:         The parent tk component. Either a frame or tkinter Tk.
            grpc_client:    The grpc client wrapper to communicate with the server.
        """
        super(BaseChatFrame, self).__init__(master)
        self._grpc_client = grpc_client
