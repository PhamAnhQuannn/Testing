import shutil

import pytest

from common import CONTENT


@pytest.fixture
def content(tmp_path):
    """A private copy of content/ that a test may break."""
    target = tmp_path / "content"
    shutil.copytree(CONTENT, target, ignore=shutil.ignore_patterns("__pycache__"))
    return target
