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
