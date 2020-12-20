import grpc
import logging
import src.server.chat_pb2_grpc as chat_pb2_grpc
import src.utils as utils

from src.server.chat_service import ChatService
from concurrent import futures

LOG_FORMAT = '[%(asctime)-15s]: %(message)s'
YAML_CONFIG_PATH = './config.yaml'


def main():
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)

    service = ChatService()

    yaml_config = utils.read_yaml_config(YAML_CONFIG_PATH)
    server_host, server_port = utils.get_server_config_from_yaml(yaml_config)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(service, server)

    logging.info('Starting Server')
    server.add_insecure_port(f'{server_host}:{server_port}')
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info('Stopping Server')
        service.stop_connection = True


if __name__ == '__main__':
    main()
