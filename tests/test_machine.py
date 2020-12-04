from task_scheduler.machine import *
from task_scheduler.task import *
import random


def test_machine_basic(test_machine: Machine):
    assert test_machine.speed == 1.2


def test_machine_tasks(test_machine: Machine):
    assert test_machine.get_time_available() == 0
    task = Task(1, 2, 3)
    assert test_machine.check_time_ready(task) == 5.4
    test_machine.add_task(task)
    assert test_machine.get_time_available() == 5.4


def test_machine_get_tasks(test_machine: Machine, test_tasks: list):
    tasks = list(sorted(test_tasks, key=lambda x: x.r_time))
    for task in tasks:
        test_machine.add_task(task)
    assert isinstance(test_machine.get_tasks(id_only=True), list)
    assert len(test_machine.get_tasks(id_only=True)) == len(test_tasks)
