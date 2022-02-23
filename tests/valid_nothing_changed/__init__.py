
import os
from itertools import chain

from .. import validate, TestBase


class ValidNothingChanged(TestBase):

    def setUp(self) -> None:
        workdir = os.path.abspath(os.path.dirname(__file__))
        self.directory_setup(workdir)
    
    def test_nothing_changed(self) -> None:
        changes = [
            validate.added(self.base, self.pr),
            validate.deleted(self.base, self.pr),
            validate.updated(self.base, self.pr)
        ]
        self.assertLength(chain(*changes), 0)