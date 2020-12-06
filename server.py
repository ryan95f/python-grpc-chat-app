import grpc
import src.server.chat_pb2_grpc as chat_pb2_grpc
from src.server.chat_service import ChatService
from concurrent import futures

def main():
    print("Starting Server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatService(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Stopping Server')

if __name__ == '__main__':
    main()