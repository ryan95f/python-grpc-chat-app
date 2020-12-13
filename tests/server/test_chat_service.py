import unittest
import grpc
import grpc_testing
import src.server.chat_pb2 as chat_pb2
import tests.utils as test_utils
from src.server.chat_service import ChatService


class TestChatService(unittest.TestCase):
    """Test case for the Chat Service"""

    def setUp(self):
        super(TestChatService, self).setUp()

        self.chat_service = ChatService()
        self.servicers = {
            chat_pb2.DESCRIPTOR.services_by_name['Chat']: self.chat_service
        }

        self.test_server = grpc_testing.server_from_dictionary(self.servicers, grpc_testing.strict_real_time())

        self.test_user_id = 1
        self.test_username = 'Test'
        self.test_message = 'Hello World'

        self.test_secondary_user_id = 2
        self.test_secondary_username = 'Another User'

    def test_connect_successfully(self):
        """Test connecting to the chat service when providing a chat user object

        Expected: An Ok response is returned where a user Id is generated
        """
        request = test_utils.create_chat_user_object(self.test_username)

        method = self.__invoke_unary_unary('connect', request)

        response, metadata, code, details = method.termination()
        self.assertEqual(response.username, self.test_username)
        self.assertIsNotNone(response.userId)
        self.assertEqual(code, grpc.StatusCode.OK)

    def __invoke_unary_unary(self, method_name, request):
        return self.test_server.invoke_unary_unary(
            method_descriptor=(chat_pb2.DESCRIPTOR
                               .services_by_name['Chat']
                               .methods_by_name[method_name]),
            invocation_metadata={},
            request=request, timeout=1)

    def test_disconnect_successfully(self):
        """Test disconnecting a user from the chat server successfully

        Expected: An Ok response with isDisconnected equalling true
        """
        self.__add_active_user(self.test_user_id, self.test_username)
        request = test_utils.create_chat_user_connected_object(self.test_user_id, self.test_username)

        method = self.__invoke_unary_unary('disconnect', request)
        response, metadata, code, details = method.termination()
        self.assertEqual(code, grpc.StatusCode.OK)
        self.assertTrue(response.isDisconnected)

    def __add_active_user(self, user_id, username):
        self.chat_service.users[user_id] = username

    def test_send_message_successfully(self):
        """Test sending a message successfully from a user

        Expected: An Ok response with the message being successfully returned
        """
        request = test_utils.create_chat_message_object(self.test_user_id, self.test_username, self.test_message)

        method = self.__invoke_unary_unary('sendMessage', request)
        response, metadata, code, details = method.termination()
        self.assertEqual(code, grpc.StatusCode.OK)
        self.assertEqual(response.message, self.test_message)

    def test_subscribe_messages_successfully(self):
        """Test subscribing successfully to incoming messages from other users

        Expected: To recieve a single message from another user
        """
        self.__add_active_user(self.test_user_id, self.test_username)

        second_user_message = test_utils.create_chat_message_object(self.test_secondary_user_id,
                                                                    self.test_secondary_username,
                                                                    self.test_message)
        self.__add_message_to_chat(second_user_message)

        request = chat_pb2.ChatUserConnected(userId=1, username='Test')
        method = self.__invoke_unary_stream('subscribeMessages', request)

        message = method.take_response()
        self.__remove_active_user(self.test_user_id)

        trailing_metadata, code, details = method.termination()
        self.assertEqual(code, grpc.StatusCode.OK)
        self.assertEqual(message.username, self.test_secondary_username)
        self.assertEqual(message.message, self.test_message)

    def __add_message_to_chat(self, message):
        self.chat_service.chats.append(message)

    def __invoke_unary_stream(self, method_name, request):
        return self.test_server.invoke_unary_stream(
            method_descriptor=(chat_pb2.DESCRIPTOR
                               .services_by_name['Chat']
                               .methods_by_name[method_name]),
            invocation_metadata={},
            request=request, timeout=1)

    def __remove_active_user(self, user_id):
        del self.chat_service.users[user_id]

    def test_subscribe_active_users_successfully(self):
        """Test subscribing successfully to active users on the server.

        Expected: A single active user who has successfully connected to the server
        """
        self.__add_active_user(self.test_user_id, self.test_username)
        self.__add_active_user(self.test_secondary_user_id, self.test_secondary_username)

        request = test_utils.create_chat_user_connected_object(self.test_user_id, self.test_username)
        method = self.__invoke_unary_stream('subscribeActiveUsers', request)

        message = method.take_response()
        self.__remove_active_user(self.test_user_id)

        trailing_metadata, code, details = method.termination()
        self.assertEqual(code, grpc.StatusCode.OK)
        self.assertEqual(message.username, self.test_secondary_username)


if __name__ == '__main__':
    unittest.main()
