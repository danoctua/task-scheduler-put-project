from abc import ABC

from main import *
from task_scheduler.cli import CLI


class MyCLI(CLI, ABC):
    """
    Use inheritance to override your validate, process, generate methods

    CLI - basic CLI class which process input from command-line interface
    ABC - implements abstract methods
    """

    def __init__(self):
        super().__init__()

    def validate(self):
        """Overriding the abstract method"""
        run_validate(last_name=self.last_name, instance_size=self.instance_size, test_mode=self.test_mode)

    def process(self):
        """Overriding the abstract method"""
        run_process(last_name=self.last_name, instance_size=self.instance_size)

    def generate(self):
        """Overriding the abstract method"""
        run_generate(last_name=self.last_name, instance_size=self.instance_size)


def main():
    cli = MyCLI()


if __name__ == '__main__':
    main()
