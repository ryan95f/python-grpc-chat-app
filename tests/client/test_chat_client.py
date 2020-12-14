import unittest
import unittest.mock as mock
import src.server.chat_pb2 as chat_pb2
import src.client.chat_client as client
import tests.utils as test_utils
from tests.mocks import MockChatStub


@mock.patch('src.server.chat_pb2_grpc.ChatStub', return_value=MockChatStub())
class TestChatClient(unittest.TestCase):
    def setUp(self):
        super(TestChatClient, self).setUp()
        self.test_user_id = 100
        self.test_username = 'Test'

    def test_connect_successfully(self, mock_stub):
        chat_client = client.ChatClient()
        result = chat_client.connect(self.test_username)

        is_chat_user_connected_instance = isinstance(result, chat_pb2.ChatUserConnected)
        self.assertTrue(is_chat_user_connected_instance)
        self.assertEqual(result.username, self.test_username)
        self.assertTrue(chat_client.is_connected)

    def test_disconnect_successfully(self, mock_stub):
        chat_client = client.ChatClient()
        chat_client.connect(self.test_username)

        is_disconnected = chat_client.disconnect()
        self.assertTrue(is_disconnected)
        self.assertFalse(chat_client.is_connected)

    def test_disconnect_when_already_disconnected(self, mock_stub):
        chat_client = client.ChatClient()
        chat_client.connect(self.test_username)
        chat_client.disconnect()

        result = chat_client.disconnect()
        self.assertTrue(result)

    def test_subscribe_messages_successfully(self, mock_stub):
        pass

    def test_subscribe_messages_when_disconnected(self, mock_stub):
        pass


if __name__ == '__main__':
    unittest.main()
