
import os

from .. import validate, TestBase


class ValidDeleted(TestBase):

    def setUp(self) -> None:
        workdir = os.path.abspath(os.path.dirname(__file__))
        self.directory_setup(workdir)
    
    def test_validate_deleted(self) -> None:
        deleted = list(validate.deleted(self.base, self.pr))
        self.assertEqual(len(deleted), 1)
        _, author, _ = deleted[0]
        self.assertEqual(author, self.committer)

    def test_empty_other(self) -> None:
        self.assertLength(validate.added(self.base, self.pr), 0)
        self.assertLength(validate.updated(self.base, self.pr), 0)
