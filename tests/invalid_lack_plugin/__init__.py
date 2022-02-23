
import os

from .. import TestBase


class InvalidLackPlugin(TestBase):

    def setUp(self) -> None:
        self.workdir = os.path.abspath(os.path.dirname(__file__))
        self.directory_setup(self.workdir)
    
    def test_invalid_lack_plugin(self) -> None:
        self.assertNotEqual(self.pr.authors.keys(), self.pr.hashings.keys())
