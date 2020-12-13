import src.server.chat_pb2 as chat_pb2


def create_chat_user_object(username):
    return chat_pb2.ChatUser(username=username)


def create_chat_user_connected_object(user_id, username):
    return chat_pb2.ChatUserConnected(userId=user_id, username=username)


def create_chat_message_object(user_id, username, message):
    return chat_pb2.ChatMessage(userId=user_id, username=username, message=message)
