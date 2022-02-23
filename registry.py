
import os
import json
import hashlib
from typing import Dict


class PluginRegistry:
    """
    Whenever a PR is submitted, GitHub Actions will checkout both main and PR branch. 
    By checking the branch's data folder as well as the ``authors.json`` file ensuring:

    0. No one can modify projects other than their own submissions.

    1. Plugins in authors.json correspond to ``plugin.json`` in data one by one.
    """

    PluginIDKey = 'id'
    ConfigDataKey, ConfigPluginKey, ConfigAuthorKey = 'data', 'plugin', 'gituser'
    Excludes = {
        '.DS_Store', '.gitignore'
    }

    def __init__(self) -> None:
        self.authors: Dict[str, str] = {}
        self.hashings: Dict[str, str] = {}

    @classmethod
    def record(cls, authors_file: str) -> 'PluginRegistry':
        """Record ``authors.json`` file for instanitiaing a :py:class:`.PluginRegistry`.

        Args:
            authors_file (str): ``author.json`` file path.

        Returns:
            PluginRegistry: plguin registry.
        """
        instance = cls()
        with open(authors_file, 'r') as handler:
            author_plugins = json.load(handler)

        # Record all plugin - author
        for item in author_plugins[cls.ConfigDataKey]:
            instance.authors[item[cls.ConfigPluginKey]
                             ] = item[cls.ConfigAuthorKey]
        return instance

    def add(self, filepath: str) -> None:
        """Validate if filename format with ``${plugin_id}.json`` 
        and calculate SHA1 for content to track updated plugins.

        Args:
            filepath (str): ``plugin.json`` file.
        """
        if os.path.basename(filepath) in self.Excludes:
            return
        with open(filepath, 'r') as handler:
            content = handler.read()
            config = json.loads(content)
        assert config[self.PluginIDKey] == os.path.basename(filepath)[
            0: -len('.json')]
        self.hashings[config[self.PluginIDKey]] = self.sha1(content)

    @staticmethod
    def sha1(data: str) -> str:
        """Return SHA1 hash of ``data``."""
        return hashlib.sha1(data.encode()).hexdigest()
