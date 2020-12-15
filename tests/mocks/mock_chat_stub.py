import tests.utils as test_utils


class MockChatStub:
    MOCK_USER_ID = 1
    MOCK_USERNAME = 'User'
    MOCK_MESSAGE = 'A test message'

    MOCK_ACTIVE_USER_ID = 2
    MOCK_ACTIVE_USERNAME = 'Active User'

    def connect(self, chat_user):
        return test_utils.create_chat_user_connected_object(self.MOCK_USER_ID, chat_user.username)

    def disconnect(self, active_user):
        return test_utils.create_chat_user_disconnected_object()

    def subscribeMessages(self, active_user):
        yield test_utils.create_chat_message_object(self.MOCK_USER_ID, self.MOCK_USERNAME, self.MOCK_MESSAGE)

    def sendMessage(self, message):
        return test_utils.create_chat_message_object(message.userId, message.username, message.message)

    def subscribeActiveUsers(self, active_user):
        yield test_utils.create_chat_active_user_object(self.MOCK_ACTIVE_USER_ID, self.MOCK_ACTIVE_USERNAME)
