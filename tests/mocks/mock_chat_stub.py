from tests.utils import create_chat_user_connected_object


class MockChatStub:
    MOCK_USER_ID = 1

    def connect(self, chat_user):
        return create_chat_user_connected_object(self.MOCK_USER_ID, chat_user.username)