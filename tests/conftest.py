import pytest
import os
import shutil


@pytest.fixture()
def test_directory():
    if os.path.exists("tmp_tests"):
        shutil.rmtree("tmp_tests")
    os.mkdir("tmp_tests")
    yield "tmp_tests"
    shutil.rmtree("tmp_tests")
