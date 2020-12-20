import yaml
import unittest
import src.utils as utils


class TestReadYamlConfig(unittest.TestCase):
    """Test case for the read_yaml_config function"""

    def test_read_yaml_config_successfully(self):
        """Test reading yaml config from a file successfully

        Expected: Yaml data from the file is returned
        """
        yaml_file = './config.yaml'
        yaml_data = utils.read_yaml_config(yaml_file)
        self.assertIsNotNone(yaml_data)

    def test_read_yaml_config_non_yaml_file(self):
        """Test reading a file when it does not have the .yaml extension

        Expected: Value error is raised when a non .yaml file is provided
        """
        fake_txt_file_path = 'test.txt'
        with self.assertRaises(ValueError):
            utils.read_yaml_config(fake_txt_file_path)

    def test_read_yaml_config_empty_string(self):
        """Test reading a config file when an empty string is provided

        Expected: Value error is raised for an empty string
        """
        with self.assertRaises(ValueError):
            utils.read_yaml_config('')

    def test_read_yaml_config_with_none(self):
        """Test reading a config file when None is provided

        Expected: Value error is raised when None is passed
        """
        with self.assertRaises(ValueError):
            utils.read_yaml_config(None)


class TestGetServerConfigFromYaml(unittest.TestCase):
    """Test case for the get_server_config_from_yaml function"""

    def setUp(self):
        super(TestGetServerConfigFromYaml, self).setUp()
        self.server_host = "test"
        self.server_port = 50051

    def test_get_server_config_from_yaml_successfully(self):
        """Test that providing valid yaml will return the server hostname and port

        Expected: The hostname and port specified in the yaml
        """
        yaml_config_str = f"""
            server:
                host: {self.server_host}
                port: {self.server_port}
        """
        yaml_data = self.__convert_to_yaml_data(yaml_config_str)

        result_host, result_port = utils.get_server_config_from_yaml(yaml_data)
        self.assertEqual(result_host, self.server_host)
        self.assertEqual(result_port, self.server_port)

    def test_get_server_config_from_yaml_with_none(self):
        """Test that providing None when yaml is expected

        Expected: Value error is raised when None is provided
        """
        with self.assertRaises(ValueError):
            utils.get_server_config_from_yaml(None)

    def test_get_server_config_from_yaml_with_none_yaml_data(self):
        """Test providing a non dictionary object into the function raises an Exception
        when a range of different data types are provided

        Expected: Value error is raised for each type
        """
        invalid_data = [1000, "a simple string", [1, 2, 3]]

        for data in invalid_data:
            with self.assertRaises(ValueError):
                utils.get_server_config_from_yaml(data)

    def test_get_server_config_from_yaml_with_missing_root_server_key(self):
        """Test getting the server config when the root key is not defined as sever:

        Expected: A key error is raised to indicate the yaml is incorrect
        """
        yaml_config_str = f"""
            test:
                host: {self.server_host}
                port: {self.server_port}
        """
        yaml_data = self.__convert_to_yaml_data(yaml_config_str)

        with self.assertRaises(KeyError):
            utils.get_server_config_from_yaml(yaml_data)

    def test_get_server_config_from_yaml_with_missing_port_key(self):
        """Test getting the server config when the expected server port key is missing

        Expected: A key error is rasied to indicate the yaml is incorrect
        """
        yaml_config_str = f"""
            server:
                host: {self.server_host}
                portNumber: {self.server_port}
        """
        yaml_data = self.__convert_to_yaml_data(yaml_config_str)

        with self.assertRaises(KeyError):
            utils.get_server_config_from_yaml(yaml_data)

    def __convert_to_yaml_data(self, data):
        return yaml.load(data, yaml.SafeLoader)


if __name__ == '__main__':
    unittest.main()
