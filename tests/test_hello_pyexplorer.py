from pyexplorer.__main__ import main
from pyexplorer.discovery import discovery_package
import pyexplorer.utilities


def test_import():
    # if this function is called it means that all modules have been imported
    pass


def test_explore_package():
    import logging
    discovery_package(logging, [])
