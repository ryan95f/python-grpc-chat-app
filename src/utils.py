import yaml


def read_yaml_config(yaml_file_path):
    """
    Read and return the configuration from a yaml file

    Args:
        yaml_file_path: The path to the yaml file

    Returns:
        The yaml data contained within the file
    """
    with open(yaml_file_path) as yamlfile:
        return yaml.load(yamlfile, yaml.SafeLoader)


def get_server_config_from_yaml(yaml_data):
    """
    Get the server configuration from yaml data

    Args:
        yaml_data: Data from a previously loaded yaml file

    Returns:
        A tuple where the first item is the server host
        and the second item is the port number
    """
    server_config = yaml_data['server']
    return server_config['host'], server_config['port']
