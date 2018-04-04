import pytest
import pathlib
import os

from PubControl.config import Config


FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))

CONFIG_INI = (
    '[SECTION1]\n'
    'key1 = value1\n'
    'key2 = 1998\n'
)


@pytest.fixture(scope='module')
def config_path(request):
    path = pathlib.Path(FOLDER_PATH) / 'config.ini'
    # Creating a new config file in the folder where these tests are also
    with path.open(mode='w+') as file:
        file.write(CONFIG_INI)

    # Creating the finalizer method, that deletes the file after the tests
    def delete_file():
        os.remove(str(path))
    request.addfinalizer(delete_file)

    # Returning the file path to the config ini file
    return str(path)


class TestConfig:

    def test_paths(self):
        config = Config()

        # Checking if all internal constants are supported through the singleton duck typing
        path_list = ['PATH', 'PROJECT_PATH', 'LOGGING_PATH', 'TEMPLATE_PATH']
        for path in path_list:
            # Checking if the constant class variable even exists
            assert hasattr(config, path)
            # Checking if it is a Path object indeed
            attribute = getattr(config, path)
            assert isinstance(attribute, pathlib.Path)

    def test_values(self, config_path):
        path = pathlib.Path(config_path)

        config = Config()
        # Changing the path to the config file and loading the new config file into the internal dict
        config.path = str(path)
        config.load()

        assert config['SECTION1']['key1'] == 'value1'
        assert config['SECTION1']['key2'] == '1998'
