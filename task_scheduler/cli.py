import abc
import sys
import time
from subprocess import check_output

"""How to use? See example in task_scheduler.py"""


class CLI:
    """
        CLI class which parses console input and set class attributes.
        This class contains next attributes:
        - (--who) last_name - choose last name for string formatting in your code. If not set: None
        - (--size) instance_size - choose specific instance size in your code. If not set: None

        To make this class working - inherit and override validate, process and generate functions.

        How to use?

        Run your python file with cli arguments:

        python3 main.py --who kowalski --size 50
        or
        python3 main.py --who kowalski
        """
    last_name = None
    instance_size = None
    input_file = None
    output_file = None
    code_path = None
    test_mode = False

    def __init__(self):
        argv = sys.argv
        if "--size" in argv:
            try:
                self.instance_size = int(argv[argv.index("--size") + 1])
            except:
                pass
        if "--who" in argv:
            last_name_idx = argv.index("--who")
            try:
                self.last_name = argv[last_name_idx + 1]
            except:
                pass
        if "--test" in argv:
            self.test_mode = True
        if "-v" in argv:
            self.input_file = argv[-1]
            self.validate()
        elif "-g" in argv:
            self.input_file = argv[-1]
            self.generate()
        elif "-p" in argv:
            self.input_file = argv[-1]
            self.process()
        elif "-r" in argv:
            self.code_path = argv[-2]
            self.input_file = argv[-1]
            self.run_algorithm()
        else:
            print("UNKNOWN MODE\n"
                  "\tHere available modes:\n"
                  "\t-p - process instances *\n"
                  "\t-v - validate instances *\n"
                  "\t-g - generate instances *\n"
                  "\t-r [code_path] [instance_file] - run algorithm with instance to process by engine\n\n"
                  "* - MUST be specified last name \"--who [LAST_NAME]\" "
                  "and COULD be specified instance size \"--size [SIZE]\"")

    @abc.abstractmethod
    def validate(self):
        """Override this method"""
        return

    @abc.abstractmethod
    def generate(self):
        """Override this method"""
        return

    @abc.abstractmethod
    def process(self):
        """Override this method"""
        return

    def run_algorithm(self):
        """Run other author algorithm, placed in codes directory (see below)"""
        start_time = time.time()
        if self.code_path.split(".")[-1] == "py":
            python_command = "python" if sys.platform == "win32" else "python3"
            res = check_output([python_command, f"codes/{self.code_path}", f"{self.input_file}"])
            print(res.decode("utf-8"))
        elif self.input_file.split(".")[-1] == "jar":
            # TODO java execution
            pass
        else:
            print("Unknown file extension. Usage: python3 [your_main_file.py] -r [code_file] [instance_file]")
        timestamp = time.time() - start_time
        print(f"Finished in {timestamp} sec")
        return
