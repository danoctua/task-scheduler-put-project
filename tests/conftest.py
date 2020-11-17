import pytest
import os
import shutil
from task_scheduler.machine import *
from task_scheduler.generator import *


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


@pytest.fixture(params=range(50, 501, 50))
def test_tasks(request) -> list:
    generator = Generator(dir_path="", last_name="")
    generator.run(request.param)
    return generator.tasks
