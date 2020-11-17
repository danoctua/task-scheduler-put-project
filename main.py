from task_scheduler.generator import Generator
from task_scheduler.validator import Validator
from task_scheduler.engine import Engine, upload_tasks
import os, sys

cur_dir_path = os.path.dirname(os.path.realpath(__file__))
last_name_ = "martsich"


def run_validate(last_name, instance_size=None, test_mode=False, mode=1):
    start = instance_size or 50
    finish = instance_size or 500
    step = 50
    result = ()
    if test_mode:
        out_last_name = "test"
    else:
        out_last_name = last_name
    for instance_size in range(start, finish + 1, step):
        in_path = f"data/in_{last_name}_{instance_size}.txt"
        with open(in_path, "r") as file:
            tasks, machines = upload_tasks(file.read(), mode=mode)
        out_path = f"data/out_{out_last_name}_{instance_size}.txt"
        with open(out_path, "r") as file:
            lines = file.read().split("\n")
            value = lines[0]
            order = "\n".join(lines[1:])
        validator = Validator(tasks=tasks, machines=machines, order=order, mode=mode)
        result = validator.validate(eval(value))
        print(f"Validation data/out_{last_name}_{instance_size}.txt: {result}")
    if instance_size:
        return result


def run_process(last_name, instance_size=None, mode=1):
    start = instance_size or 50
    finish = instance_size or 500
    step = 50
    for instance_size in range(start, finish + 1, step):
        test_path = f"data/in_{last_name}_{instance_size}.txt"
        with open(test_path, "r") as file:
            tasks, machines = upload_tasks(file.read(), mode=mode)
        engine = Engine(tasks=tasks, mode=mode, machines=machines)
        engine.run()
        engine.save_to_file(f"data/out_{last_name}_{instance_size}.txt")
        print(f"Processed for instance of {instance_size}")


def run_generate(last_name, instance_size=None, mode=1):
    start = instance_size or 50
    finish = instance_size or 500
    step = 50
    generator = Generator("data", last_name, mode=mode, machines_number=5)
    for instance_size in range(start, finish + 1, step):
        generator.run(instance_size)
        generator.write_to_file()


if __name__ == '__main__':
    # test_validate()
    # generate_test_out()
    # generate()
    # test_engine(50)
    # generate_output()
    # run_process(last_name="martsich", instance_size=50, mode=2)
    run_validate(last_name="martsich", instance_size=500, test_mode=True, mode=2)
