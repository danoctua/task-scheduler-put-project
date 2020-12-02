from task_scheduler.task import *
import pytest


def test_basic_task_5():
    task = Task(4, 5, 6, 7, 8)
    assert task.task_id == 4
    assert task.p_time == 5
    assert task.r_time == 6
    assert task.d_time == 7
    assert task.w == 8


def test_basic_task_4():
    task = Task(4, 5, 6, 7)
    print(task)
    assert task.task_id == 4
    assert task.p_time == 5
    assert task.r_time == 6
    assert task.d_time == 7
    assert not task.w


def test_basic_task_3():
    task = Task(4, 5, 6)
    assert task.task_id == 4
    assert task.p_time == 5
    assert task.r_time == 6
    assert not task.d_time
    assert not task.w


def test_basic_task_2():
    task = Task(4, 5)
    assert not task.task_id


def test_basic_task_parse_input():
    task = Task()
    task.parse_input(1, "4 5")
    assert task.p_time == 4
    assert task.r_time == 5


def test_task_parse_input_mode_1():
    task = Task()
    task.parse_input(task_id=1, input_str="4 5 6 7")
    assert task.p_time == 4
    assert task.r_time == 5
    assert task.d_time == 6
    assert task.w == 7


def test_task_parse_input_mode_2():
    task = Task()
    task.parse_input(task_id=1, input_str="4 5")
    assert task.p_time == 4
    assert task.r_time == 5
    assert not task.d_time
    assert not task.w


def test_task_parse_input_mode_3():
    task = Task()
    task.parse_input(task_id=1, input_str="4 5 6 7 8")
    assert task.p_times == [4, 5, 6]
    assert task.d_time == 7
    assert task.w == 8
    assert not task.p_time
    assert not task.r_time
