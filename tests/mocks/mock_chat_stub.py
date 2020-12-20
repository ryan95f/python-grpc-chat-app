import tests.common as tests_common


class MockChatStub:
    """Mock of the chat stub to emulate communicating with the chat server"""

    MOCK_USER_ID = 1
    MOCK_USERNAME = 'User'
    MOCK_MESSAGE = 'A test message'

    MOCK_ACTIVE_USER_ID = 2
    MOCK_ACTIVE_USERNAME = 'Active User'

    def connect(self, chat_user):
        """Mock connecting to the server

        Args:
            chat_user: The user's username who is connecting to the server

        Returns:
            A chat active user object
        """
        return tests_common.create_chat_user_connected_object(self.MOCK_USER_ID, chat_user.username)

    def disconnect(self, active_user):
        """Mock disconnecting from the server

        Args:
            active_user: The chat active user who is disconnecting

        Returns:
            A chat user disconnected object with isDisconnected set to true
        """
        return tests_common.create_chat_user_disconnected_object()

    def subscribeMessages(self, active_user):
        """Mock subscribing to messages from other users on the server

        Args:
            active_user: The chat active user

        Args:
            Generator that contains a single chat message object
        """
        yield tests_common.create_chat_message_object(self.MOCK_USER_ID, self.MOCK_USERNAME, self.MOCK_MESSAGE)

    def sendMessage(self, message):
        """Mock sending a message to the chat server

        Args:
            message: A chat message object

        Returns:
            The chat message object that was send to the server.
            Indicating the message was recieved
        """
        return tests_common.create_chat_message_object(message.userId, message.username, message.message)

    def subscribeActiveUsers(self, active_user):
        """Mock subscribing to other active users on the server

        Args:
            active_user: The chat active user

        Returns:
            Generator that contains a single active user object
        """
        yield tests_common.create_chat_active_user_object(self.MOCK_ACTIVE_USER_ID, self.MOCK_ACTIVE_USERNAME)
