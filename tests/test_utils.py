import yaml
import unittest
import src.utils as utils


class TestReadYamlConfig(unittest.TestCase):

    def test_read_yaml_config_successfully(self):
        yaml_file = './config.yaml'
        yaml_data = utils.read_yaml_config(yaml_file)
        self.assertIsNotNone(yaml_data)

    def test_read_yaml_config_non_yaml_file(self):
        fake_txt_file_path = 'test.txt'
        with self.assertRaises(ValueError):
            utils.read_yaml_config(fake_txt_file_path)

    def test_read_yaml_config_empty_string(self):
        with self.assertRaises(ValueError):
            utils.read_yaml_config('')

    def test_read_yaml_config_with_none(self):
        with self.assertRaises(ValueError):
            utils.read_yaml_config(None)


class TestGetServerConfigFromYaml(unittest.TestCase):
    def setUp(self):
        super(TestGetServerConfigFromYaml, self).setUp()
        self.server_host = "test"
        self.server_port = 50051

    def test_get_server_config_from_yaml_successfully(self):
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
        with self.assertRaises(ValueError):
            utils.get_server_config_from_yaml(None)

    def test_get_server_config_from_yaml_with_none_yaml_data(self):
        number = 1000
        with self.assertRaises(ValueError):
            utils.get_server_config_from_yaml(number)

    def test_get_server_config_from_yaml_with_missing_root_server_key(self):
        yaml_config_str = f"""
            test:
                host: {self.server_host}
                port: {self.server_port}
        """
        yaml_data = self.__convert_to_yaml_data(yaml_config_str)

        with self.assertRaises(KeyError):
            utils.get_server_config_from_yaml(yaml_data)

    def test_get_server_config_from_yaml_with_missing_port_key(self):
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
