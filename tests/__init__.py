
from typing import Iterable

import os
import sys
import unittest

dirname = os.path.dirname(__file__)
workdir = os.path.abspath(dirname)
sys.path.append(os.path.realpath(os.path.join(dirname)))
sys.path.append(os.path.realpath(os.path.join(dirname, '..')))

try:
    import validate
    import registry
except:
    exit(1)


class SequentialTestLoader(unittest.TestLoader):
    def getTestCaseNames(self, testCaseClass):
        test_names = super().getTestCaseNames(testCaseClass)
        testcase_methods = list(testCaseClass.__dict__.keys())
        test_names.sort(key=testcase_methods.index)  # type: ignore
        return test_names


class TestBase(unittest.TestCase):

    BaseDir, PRDir = './base', './pr'
    AuthorConfig = 'authors.json'
    DataDir = 'data'

    def directory_setup(self, workdir: str) -> None:
        os.chdir(workdir)
        basedir = os.path.abspath(self.BaseDir)
        prdir = os.path.abspath(self.PRDir)
        self.committer = 'doge'
        self.base = registry.PluginRegistry.record(
            os.path.join(basedir, self.AuthorConfig))
        self.pr = registry.PluginRegistry.record(
            os.path.join(prdir, self.AuthorConfig))
        if os.path.isdir(basedir):
            for file in os.listdir(os.path.join(basedir, self.DataDir)):
                self.base.add(os.path.join(basedir, self.DataDir, file))
        for file in os.listdir(os.path.join(prdir, self.DataDir)):
            self.pr.add(os.path.join(prdir, self.DataDir, file))

    def assertLength(self, obj: Iterable, length: int, msg: str = '') -> None:
        self.assertEqual(len(list(obj)), length, msg)


def suite() -> unittest.TestSuite:

    from .valid_added import ValidAdded
    from .valid_nothing_changed import ValidNothingChanged
    from .valid_deleted import ValidDeleted
    from .valid_updated import ValidUpdated
    from .invalid_lack_config import InvalidLackConfig
    from .invalid_lack_plugin import InvalidLackPlugin
    from .invalid_unmatched_plugin_id import InvalidUnmatchedPluginID
    from .invalid_delete_denied import InvalidDeletedDined

    testcases = [
        ValidAdded, ValidNothingChanged,
        ValidDeleted, ValidUpdated,
        InvalidUnmatchedPluginID,
        InvalidLackPlugin, InvalidLackConfig,
        InvalidDeletedDined
    ]

    loader = SequentialTestLoader()
    suite = unittest.TestSuite()

    for testcase in testcases:
        suite.addTests(loader.loadTestsFromTestCase(testcase))
    return suite
