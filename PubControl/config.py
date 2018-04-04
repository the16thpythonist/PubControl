import os
import pathlib
import configparser


class Config:

    class _Config:

        # These are constants, that are relevant to the whole project
        PATH = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        TEMPLATE_PATH = PATH / 'templates'

        PROJECT_PATH = pathlib.Path('/home/jonas/PycharmProjects/PubControl/PubControl')
        LOGGING_PATH = PROJECT_PATH / 'logs'

        def __init__(self):
            # Loading the
            self.path = str(self.PROJECT_PATH / 'config.ini')
            self.dict = configparser.ConfigParser()
            self.dict.read(self.path)

        def load(self):
            self.dict = configparser.ConfigParser()
            self.dict.read(self.path)

        def save(self):
            self.dict.write(self.path)

        def __getitem__(self, item):
            return self.dict[item]

        def __setitem__(self, key, value):
            self.dict[key] = value

    _instance = None

    def __init__(self):
        if self._instance is None:
            setattr(Config, '_instance', Config._Config())

    def __getitem__(self, item):
        return self._instance[item]

    def __setitem__(self, key, value):
        self._instance[key] = value

    def __setattr__(self, key, value):
        if self._instance is not None:
            setattr(self._instance, key, value)

    def __getattr__(self, item):
        return getattr(self._instance, item)