import unittest
import grpc
import grpc_testing
import src.server.chat_pb2 as chat_pb2
from src.server.chat_service import ChatService


class TestSample(unittest.TestCase):
    def setUp(self):
        super(TestSample, self).setUp()
        self.chat_service = ChatService()
        self.servicers = {
            chat_pb2.DESCRIPTOR.services_by_name['Chat']: self.chat_service
        }

        self.test_server = grpc_testing.server_from_dictionary(self.servicers, grpc_testing.strict_real_time())

    def test_connect(self):
        request = chat_pb2.ChatUser(username='Test')

        method = self.test_server.invoke_unary_unary(
            method_descriptor=(chat_pb2.DESCRIPTOR
                               .services_by_name['Chat']
                               .methods_by_name['connect']),
            invocation_metadata={},
            request=request, timeout=1)

        response, metadata, code, details = method.termination()
        self.assertEqual(response.username, 'Test')
        self.assertIsNotNone(response.userId)
        self.assertEqual(code, grpc.StatusCode.OK)

    def test_disconnect(self):
        self.chat_service.users[1] = 'Test'
        request = chat_pb2.ChatUserConnected(userId=1, username='Test')

        method = self.test_server.invoke_unary_unary(
            method_descriptor=(chat_pb2.DESCRIPTOR
                               .services_by_name['Chat']
                               .methods_by_name['disconnect']),
            invocation_metadata={},
            request=request, timeout=1)

        response, metadata, code, details = method.termination()
        self.assertEqual(code, grpc.StatusCode.OK)


if __name__ == '__main__':
    unittest.main()
