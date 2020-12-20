import types
import unittest
import unittest.mock as mock
import src.server.chat_pb2 as chat_pb2
import src.client.chat_client as client
import src.client.exceptions as client_exceptions
import tests.common as tests_common
from tests.mocks import MockChatStub


class TestChatClient(unittest.TestCase):
    """Test case for the ChatClient object that is a wrapper
    around the gRPC stub to make connecting to the server easier
    """

    def setUp(self):
        super(TestChatClient, self).setUp()
        self.test_user_id = 100
        self.test_username = 'Test'
        self.test_message = 'Hello World'

        self.patcher = mock.patch('src.server.chat_pb2_grpc.ChatStub', return_value=MockChatStub())
        self.patcher.start()

        self.chat_client = client.ChatClient()

    def tearDown(self):
        super(TestChatClient, self).tearDown()
        self.patcher.stop()

    def test_connect_successfully(self):
        """Test connecting to the chat server by passing the user's username
        to the chat server.

        Expected: The chat client returns a True to indicate the user has
                  connected to the server and the internal state of the chat client
                  aligns with the is_connected flag set to true
        """
        result = self.__connect_client()

        is_chat_user_connected_instance = isinstance(result, chat_pb2.ChatUserConnected)
        self.assertTrue(is_chat_user_connected_instance)
        self.assertEqual(result.username, self.test_username)

    def __connect_client(self):
        return self.chat_client.connect(self.test_username)

    def test_disconnect_successfully(self):
        """Test disconnecting a user from the chat server successfully

        Expected: The chat client returns True to indicate that the
                  server has successfully disconnected and the internal
                  state of the chat client aligns with the is_connected flag
                  set to false
        """
        self.__connect_client()

        is_disconnected = self.chat_client.disconnect()
        self.assertTrue(is_disconnected)
        self.assertFalse(self.chat_client.is_connected)

    def test_disconnect_when_already_disconnected(self):
        """Test trying to disconnect when the user has already
           disconnected from the server.

        Expected: The chat client return true to indicate
                  the user is already disconnected
        """
        self.__connect_client()
        self.chat_client.disconnect()

        result = self.chat_client.disconnect()
        self.assertTrue(result)

    def test_subscribe_messages_successfully(self):
        """Test subscribing to incoming messages from the server

        Expected: The chat client should return a generator for incoming
                  messages from other users
        """
        expected_messages_length = 1
        self.__connect_client()

        result = self.chat_client.subscribe_messages()
        self.assertIsInstance(result, types.GeneratorType)

    def test_subscribe_messages_when_disconnected(self):
        """Test subscribing to incoming messages when the client
        is disconnected from the chat server

        Expected: The chat client raises a NotConnectorError when
                  attemtping to subscribe to messages
        """
        with self.assertRaises(client_exceptions.NotConnectedError):
            self.chat_client.subscribe_messages()

    def test_send_message_successfully(self):
        """Test sending a message through the chat client

        Expected: The chat client responds with the gRPC
                  message object that was sent to the server
        """
        self.__connect_client()

        message = self.__create_mock_grpc_chat_message()
        result = self.chat_client.send_message(message)

        self.assertEqual(result.username, message.username)
        self.assertEqual(result.message, message.message)

    def __create_mock_grpc_chat_message(self):
        return tests_common.create_chat_message_object(self.test_user_id, self.test_username, self.test_message)

    def test_send_message_when_disconnected(self):
        """Test sending a message through the chat client when the
        user is disconnected from the server

        Expected: The chat client raises a NotConnectorError when
                  attemtping to send a message
        """
        message = self.__create_mock_grpc_chat_message()
        with self.assertRaises(client_exceptions.NotConnectedError):
            self.chat_client.send_message(message)

    def test_subscrube_active_users_successfully(self):
        """Test subscribing to active users on the chat server

        Expected: The chat client should return a generator for other
                  active users on the server
        """
        self.__connect_client()

        result = self.chat_client.subscribe_active_users()
        self.assertIsInstance(result, types.GeneratorType)

    def test_subscrube_active_users_when_disconnected(self):
        """Test subscribing to active users when the client
        is disconnected from the chat server

        Expected: The chat client raises a NotConnectorError when
                  attemtping to subscribe to active users
        """
        with self.assertRaises(client_exceptions.NotConnectedError):
            self.chat_client.subscribe_active_users()


if __name__ == '__main__':
    unittest.main()
