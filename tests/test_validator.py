from task_scheduler.validator import *
from task_scheduler.engine import *


def test_validator_basic(test_tasks):
    validator = Validator(tasks=test_tasks, order=" ".join([str(x) for x in list(range(1, len(test_tasks)+1))]))
    valid, correct, _ = validator.validate(0)
    assert valid
    assert not correct


# FIXME: not passing
def test_validator_mode_1(test_tasks):
    engine = Engine(mode=1, tasks=test_tasks)
    engine.run()
    validator = Validator(mode=1, tasks=test_tasks, order=engine.get_order_str())
    valid, correct, result = validator.validate(engine.result)
    assert valid
    assert result == engine.result
    assert correct
