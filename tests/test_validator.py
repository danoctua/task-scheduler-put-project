from task_scheduler.validator import *


def test_validator_basic(test_tasks):
    validator = Validator(tasks=test_tasks)
