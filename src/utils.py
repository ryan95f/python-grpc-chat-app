import re
import yaml

_YAML_FILE_EXTENSION_REGEX = re.compile(r'\w+.yaml')


def read_yaml_config(yaml_file_path):
    """
    Read and return the configuration from a yaml file

    Args:
        yaml_file_path: The path to the yaml file

    Returns:
        The yaml data contained within the file

    Rasies:
        ValueError: When the provided file path does not
                    have a `.yaml` extension or is None.
    """
    if yaml_file_path is None:
        raise ValueError('Yaml file path cannot be none!')

    is_yaml_file = _YAML_FILE_EXTENSION_REGEX.search(yaml_file_path)

    if is_yaml_file is None:
        raise ValueError(f'{yaml_file_path} is not a yaml file!')

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

    Raises:
        ValueError: If the yaml data is not in a dictionary format
        KeyError:   If any of the expected keys is missing. Indicating
                    the yaml is malformed.
    """
    if (yaml_data is None) or (not isinstance(yaml_data, dict)):
        raise ValueError('Yaml data needs to be a dict type!')

    server_config = yaml_data['server']
    return server_config['host'], server_config['port']
