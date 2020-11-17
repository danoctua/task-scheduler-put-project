from task_scheduler.generator import *
from task_scheduler.task import *


def test_generator_file_create(test_directory):
    instance_size = 50
    last_name = "smith"
    generator = Generator(dir_path=test_directory, last_name=last_name, mode=1)
    generator.run(instance_size)
    generator.write_to_file()
    assert generator.to_order() == "0\n" + " ".join([str(x) for x in range(1, 51)])
    assert os.path.exists(os.path.join(test_directory, f"in_{last_name}_{instance_size}.txt"))


def test_generator_basic_mode_1(test_directory):
    instance_size = 50
    last_name = "smith"
    generator = Generator(dir_path=test_directory, last_name=last_name, mode=1)
    generator.run(instance_size)
    generator.write_to_file()
    assert len(generator.tasks) == instance_size
    assert generator.to_order() == "0\n" + " ".join([str(x) for x in range(1, 51)])
    assert all([isinstance(x, Task) for x in generator.tasks])


def test_generator_basic_mode_2(test_directory):
    instance_size = 500
    machines_number = 5
    last_name = "smith"
    generator = Generator(dir_path=test_directory, machines_number=machines_number, last_name=last_name, mode=2)
    generator.run(instance_size)
    generator.write_to_file()
    assert len(generator.tasks) == instance_size
    assert len(generator.machines) == machines_number
    assert 1.0 in generator.machines
    assert all([isinstance(x, Task) for x in generator.tasks])
