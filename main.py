from task_scheduler.generator import Generator
from task_scheduler.validator import Validator
from task_scheduler.engine import Engine
import os
import sys
from task_scheduler.task import Task

cur_dir_path = os.path.dirname(os.path.realpath(__file__))

last_name_ = "martsich"


def upload_tasks(input_str: str) -> list:
    lines = input_str.split("\n")
    result = []
    n = lines[0]
    try:
        n = int(n)
    except ValueError:
        print("Wrong instances count")
        return result
    for idx in range(1, n+1):
        new_task = Task()
        new_task.parse_input(idx, lines[idx])
        result.append(new_task)
    return result


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
        tasks = upload_tasks(file.read())
    validator = Validator(tasks=tasks, order=" ".join([str(x) for x in range(1, 50)]))
    result = validator.validate(169)
    print(result)


def test_engine(instance_size):
    last_name = last_name_
    test_path = f"data/in_{last_name}_{instance_size}.txt"
    with open(test_path, "r") as file:
        tasks = upload_tasks(file.read())
    engine = Engine(tasks=tasks, instance_size=instance_size)
    result = engine.run()
    engine.save_to_file(f"data/out_{last_name}_{instance_size}.txt")
    validator = Validator(tasks=tasks, order=" ".join([str(x) for x in result]))
    result = validator.calculate()
    print(instance_size, sum([x.w for x in tasks]), result)


def generate_test_out():
    for instance_size in range(50, 501, 50):
        result = "0\n"
        result += " ".join([str(x) for x in range(1, instance_size+1)])
        with open(f"data/out_test_{instance_size}.txt", "w") as file:
            file.write(result)


def generate_output():
    for instance_size in range(50, 501, 50):
        test_engine(instance_size)


def run_validate(last_name):
    for instance_size in range(50, 501, 50):
        in_path = f"data/in_{last_name}_{instance_size}.txt"
        with open(in_path, "r") as file:
            tasks = upload_tasks(file.read())
        out_path = f"data/out_{last_name}_{instance_size}.txt"
        with open(out_path, "r") as file:
            value, order = file.read().splitlines()[:2]
        validator = Validator(tasks=tasks, order=order)
        result = validator.validate(int(value))
        print(f"Validation data/out_{last_name}_{instance_size}.txt: {result}")
    return


if __name__ == '__main__':
    # test_validate()
    # generate_test_out()
    # generate()
    # test_engine(50)
    generate_output()
