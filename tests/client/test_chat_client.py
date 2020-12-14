import unittest
import unittest.mock as mock
import src.server.chat_pb2 as chat_pb2
import src.client.chat_client as client
from tests.mocks import MockChatStub


@mock.patch('src.server.chat_pb2_grpc.ChatStub', return_value=MockChatStub())
class TestChatClient(unittest.TestCase):
    def setUp(self):
        super(TestChatClient, self).setUp()
        self.test_username = 'Test'

    def test_connect_successfully(self, mock_stub):
        chat_client = client.ChatClient()
        result = chat_client.connect(self.test_username)

        is_chat_user_connected_type = isinstance(result, chat_pb2.ChatUserConnected)
        self.assertTrue(is_chat_user_connected_type)
        self.assertEqual(result.username, self.test_username)
        self.assertTrue(chat_client.is_connected)


if __name__ == '__main__':
    unittest.main()
