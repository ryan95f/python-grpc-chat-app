import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc
from tests.utils import create_chat_user_connected_object


class MockChatService(chat_pb2_grpc.ChatServicer):
    MOCK_USER_ID = 100
    MOCK_USERNAME = 'Test'

    def connect(self, request, context):
        return create_chat_user_connected_object(MOCK_USER_ID, MOCK_USERNAME)
