from abc import ABC

from main import *
from task_scheduler.cli import CLI


class MyCLI(CLI, ABC):
    """
    Use inheritance to override your validate, process, generate methods
    """

    def __init__(self):
        super().__init__()

    def validate(self):
        run_validate(last_name=self.last_name, instance_size=self.instance_size)

    def process(self):
        run_process(last_name=self.last_name, instance_size=self.instance_size)

    def generate(self):
        run_generate(last_name=self.last_name, instance_size=self.instance_size)


def main():
    cli = MyCLI()


if __name__ == '__main__':
    main()
