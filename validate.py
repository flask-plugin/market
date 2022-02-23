
import os
import sys
import enum
from itertools import chain
from typing import Iterator, Tuple

from registry import PluginRegistry


Config, DataDir = 'authors.json', 'data'


@enum.unique
class Operation(enum.Enum):
    Added = 0
    Deleted = 1
    Updated = 2


def updated(old: PluginRegistry, new: PluginRegistry) -> Iterator[Tuple[str, str, Operation]]:
    for plugin, sha1 in new.hashings.items():
        if plugin in old.hashings and sha1 != old.hashings[plugin]:
            yield plugin, old.authors[plugin], Operation.Updated


def added(old: PluginRegistry, new: PluginRegistry) -> Iterator[Tuple[str, str, Operation]]:
    for plugin, author in new.authors.items():
        if plugin not in old.authors:
            yield plugin, author, Operation.Added
            continue
        assert author == old.authors[plugin]


def deleted(old: PluginRegistry, new: PluginRegistry) -> Iterator[Tuple[str, str, Operation]]:
    for plugin, author in old.authors.items():
        if plugin not in new.authors:
            yield plugin, author, Operation.Deleted


def main(basedir: str, prdir: str, committer: str) -> None:

    BaseDataDir, PRDataDir = os.path.join(
        BaseDir, DataDir), os.path.join(PRDir, DataDir)
    BaseConfigFile, PRConfigFile = os.path.join(
        BaseDir, Config), os.path.join(PRDir, Config)

    # Build registry
    base = PluginRegistry.record(BaseConfigFile)
    pr = PluginRegistry.record(PRConfigFile)

    # Add record to registry
    if os.path.isdir(BaseDataDir):
        for file in os.listdir(BaseDataDir):
            base.add(os.path.join(BaseDataDir, file))
    for file in os.listdir(PRDataDir):
        pr.add(os.path.join(PRDataDir, file))
    assert pr.authors.keys() == pr.hashings.keys()

    # Check if changes author is committer
    for plugin, author, operation in chain(
            added(base, pr), deleted(base, pr), updated(base, pr)):
        assert Committer == author
        print(f'{author} - {operation.name}: {plugin}')


if __name__ == '__main__':

    # Configs
    assert len(sys.argv) == 4
    BaseDir, PRDir, Committer = sys.argv[1], sys.argv[2], sys.argv[3]
    main(BaseDir, PRDir, Committer)
