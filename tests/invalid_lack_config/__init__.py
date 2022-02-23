
import os

from .. import TestBase


class InvalidLackConfig(TestBase):

    def setUp(self) -> None:
        workdir = os.path.abspath(os.path.dirname(__file__))
        self.directory_setup(workdir)
    
    def test_invalid_lack_config(self) -> None:
        self.assertNotEqual(self.pr.authors.keys(), self.pr.hashings.keys())
        