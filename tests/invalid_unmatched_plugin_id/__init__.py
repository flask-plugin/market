
import os

from .. import TestBase


class InvalidUnmatchedPluginID(TestBase):

    def test_invalid_unmatched_plugin_id(self) -> None:
        workdir = os.path.abspath(os.path.dirname(__file__))
        self.assertRaises(AssertionError, lambda: self.directory_setup(workdir))