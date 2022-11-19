
import os
import json
from typing import Dict
from functools import lru_cache as cache

import requests
import jsonschema

PluginJsonSchemaURL = "https://raw.githubusercontent.com/flask-plugin/flask-plugin/main/src/plugin.schema.json"


@cache(None)
def schema() -> Dict:
    """Return Flask Plugin JSON Schema. Cached property."""
    response = requests.get(PluginJsonSchemaURL)
    return json.loads(response.text)


class PluginAdder:

    IDKey, ConfigFilename = 'id', 'plugin.json'

    def __init__(self, author: str, dirpath: str) -> None:
        self.author, self.dirpath = author, dirpath

    @property
    @cache(None)
    def config(self) -> Dict:
        """Validate and return plugin config. Cached property."""
        filepath = os.path.join(self.dirpath, self.ConfigFilename)
        with open(filepath, 'r') as handler:
            config = json.load(handler)
            jsonschema.validate(config, schema=schema())
            return config

    @property
    def id_(self) -> str:
        """Return plugin id."""
        return self.config[self.IDKey]


class Manager:
    """Support CLI plugin management.

    Basically you should call :py:meth:`Manager.open(authors, plugins)` when openning manager.
    Using :py:meth:`Manager`

    Args:
        authors (Dict): ``authors.json`` config.
        record (str): ``authors.json`` filepath.
        plugins (str): cataloge storing all ``plugin.json`` files.
    """

    PluginConfigs = 'data'
    AuthorsRecordsFile = 'authors.json'
    AuthorsRecordAuthorKey = 'gituser'
    AuthorsRecordPluginKey = 'plugin'

    def __init__(self) -> None:
        workdir = os.path.dirname(os.path.abspath(__file__))
        self._plugins = os.path.join(workdir, self.PluginConfigs)
        self._authors = os.path.join(workdir, self.AuthorsRecordsFile)

    def _config_filename(self, id_: str) -> str:
        """Return target plugin config filename."""
        return os.path.join(self._plugins, id_ + '.json')

    def add(self, author: str, dirpath: str) -> None:
        """Add plugin config to database."""
        adder = PluginAdder(author, dirpath)
        filename = self._config_filename(adder.id_)
        if os.path.isfile(filename):
            raise ValueError('Plugin id already exists, using updated instead please')
        with open(self._config_filename(adder.id_), 'w') as handler:
            json.dump(adder.config, handler)
        
