from task_scheduler.generator import *
from task_scheduler.task import *


def test_generator_file_create(test_directory):
    instance_size = 50
    last_name = "smith"
    generator = Generator(dir_path=test_directory, last_name=last_name, mode=1)
    generator.run(instance_size)
    assert os.path.exists(os.path.join(test_directory, f"in_{last_name}_{instance_size}.txt"))


def test_generator_basic_mode_1(test_directory):
    instance_size = 50
    last_name = "smith"
    generator = Generator(dir_path=test_directory, last_name=last_name, mode=1)
    generator.run(instance_size)
    assert len(generator.tasks) == instance_size
    assert all([isinstance(x, Task) for x in generator.tasks])


def test_generator_basic_mode_2(test_directory):
    instance_size = 500
    engines_number = 5
    last_name = "smith"
    generator = Generator(dir_path=test_directory, engines_number=engines_number, last_name=last_name, mode=2)
    generator.run(instance_size)
    assert len(generator.tasks) == instance_size
    assert len(generator.engines) == engines_number
    assert 1.0 in generator.engines
    assert all([isinstance(x, Task) for x in generator.tasks])
