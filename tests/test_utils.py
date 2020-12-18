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
    def test_get_server_config_from_yaml_successfully(self):
        pass

    def test_get_server_config_from_yaml_with_none(self):
        pass

    def test_get_server_config_from_yaml_with_none_yaml_data(self):
        pass

    def test_get_server_config_from_yaml_with_missing_expected_keys(self):
        pass


if __name__ == '__main__':
    unittest.main()
