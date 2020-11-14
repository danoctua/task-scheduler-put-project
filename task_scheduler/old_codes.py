from task_scheduler.generator import Generator
from task_scheduler.validator import Validator
from task_scheduler.engine import Engine, upload_tasks
import os

cur_dir_path = os.path.dirname(os.path.realpath(__file__))

last_name_ = "martsich"

# test functions


def generate():
    last_name = last_name_
    generator = Generator("data", last_name)
    for instances in range(50, 501, 50):
        generator.run(instances)


def test_validate():
    instance_size = 50
    last_name = last_name_
    test_path = f"data/in_{last_name}_{instance_size}.txt"
    with open(test_path, "r") as file:
        tasks, machines = upload_tasks(file.read())
    validator = Validator(tasks=tasks, order=" ".join([str(x) for x in range(1, 50)]))
    result = validator.validate(169)
    print(result)


def test_engine(instance_size):
    last_name = "martsich"
    test_path = f"data/in_{last_name}_{instance_size}.txt"
    with open(test_path, "r") as file:
        tasks, machines = upload_tasks(file.read(), mode=2)
    engine = Engine(tasks=tasks, mode=2, machines=machines)
    result = engine.run()
    engine.save_to_file(f"data/out_{last_name}_{instance_size}.txt")
    validator = Validator(tasks=tasks, machines=machines, mode=2, order="\n".join([" ".join([str(y) for y in x]) for x in result]))
    result = validator.calculate()
    print(instance_size, result)


def generate_test_out():
    for instance_size in range(50, 501, 50):
        result = "0\n"
        result += " ".join([str(x) for x in range(1, instance_size+1)])
        with open(f"data/out_test_{instance_size}.txt", "w") as file:
            file.write(result)


def generate_output():
    for instance_size in range(50, 501, 50):
        test_engine(instance_size)


if __name__ == '__main__':
    test_engine(400)
