import pytest
import os
import shutil
from task_scheduler.machine import *


@pytest.fixture()
def test_directory():
    if os.path.exists("tmp_tests"):
        shutil.rmtree("tmp_tests")
    os.mkdir("tmp_tests")
    yield "tmp_tests"
    shutil.rmtree("tmp_tests")


@pytest.fixture()
def test_machine() -> Machine:
    speed = 1.2
    machine = Machine(machine_id=1, speed=speed)
    return machine
