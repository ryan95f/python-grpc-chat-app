import unittest
import unittest.mock as mock
import grpc_testing
import src.server.chat_pb2 as chat_pb2
from src.client import chat_client
from tests.mocks.mock_chat_serivce import MockChatService


class TestChatClient(unittest.TestCase):
    def setUp(self):
        super(TestChatClient, self).setUp()

        self.chat_service = MockChatService()
        self.servicers = {
            chat_pb2.DESCRIPTOR.services_by_name['Chat']: self.chat_service
        }
        self.test_channel = grpc_testing.channel(self.servicers, grpc_testing.strict_real_time())
        self.chat_client = chat_client.ChatClient(self.test_channel)

    def test_simpple(self):
        results = self.chat_client.connect('Test')


if __name__ == '__main__':
    unittest.main()
