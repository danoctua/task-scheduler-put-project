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


def test_machine_count_mode_3():
    machines_number = 3
    tasks_number = 5
    # p_times == [4, 5, 6]
    # d_time == 7
    # w == 8
    machines = [Machine(machine_id=i, speed=1) for i in range(machines_number)]
    tasks = [Task() for _ in range(tasks_number)]
    [task.parse_input(task_id=task_id, input_str="4 5 6 7 8") for task_id, task in enumerate(tasks)]
    for machine_id, machine in enumerate(machines):
        for task_id, task in enumerate(tasks):
            machine.add_task(
                task,
                p_time=task.p_times[machine_id],
                min_start_time=machines[machine_id - 1].get_time_available(task_id) if machine_id else 0)
    assert machines[-1].get_time_over_weighted() == 800.0
