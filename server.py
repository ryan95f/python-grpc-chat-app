import grpc
import logging
import src.server.chat_pb2_grpc as chat_pb2_grpc

from src.server.chat_service import ChatService
from concurrent import futures

LOG_FORMAT = '[%(asctime)-15s]: %(message)s'


def main():
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    logging.info('Starting Server')
    service = ChatService()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(service, server)

    server.add_insecure_port('localhost:50051')
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info('Stopping Server')
        service.stop_connection = True


if __name__ == '__main__':
    main()
