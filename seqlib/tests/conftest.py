import os.path
import pytest


@pytest.fixture
def data_folder():
    return os.path.abspath(os.path.dirname(__file__))
