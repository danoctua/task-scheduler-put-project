from abc import ABC

from main import *
from task_scheduler.cli import CLI
from task_scheduler import CLIColors
import time
from subprocess import check_output
import pandas as pd
import datetime


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
        if self.last_names:
            valid_ls = []
            equal_ls = []
            criteria_ls = []
            start = self.instance_size or 50
            finish = self.instance_size or 500 + 1
            errors_ls = []
            for last_name_ in self.last_names:
                for i_size in range(start, finish, 50):
                    error = ""
                    try:
                        result = run_validate(last_name=last_name_, instance_size=i_size,
                                              test_mode=self.test_mode, mode=self.mode)
                    except Exception as exp:
                        print(exp)
                        result = (False, False, "")
                        error = exp
                    valid_ls.append(result[0])
                    equal_ls.append(result[1])
                    criteria_ls.append(str(result[2]).replace(".", ","))
                    errors_ls.append(error)
            save_to_csv(last_names=self.last_names, calculated=criteria_ls, valid=valid_ls, equal=equal_ls,
                        instances=[self.instance_size] if self.instance_size else list(range(50, 501, 50)),
                        measures=[None for _ in range(len(valid_ls))],
                        errors=errors_ls)
        if self.last_name:
            run_validate(last_name=self.last_name, instance_size=self.instance_size,
                         test_mode=self.test_mode, mode=self.mode)

    def process(self):
        """Overriding the abstract method"""
        run_process(last_name=self.last_name, last_names=self.last_names,
                    instance_size=self.instance_size, mode=self.mode)

    def generate(self):
        """Overriding the abstract method"""
        run_generate(last_name=self.last_name, instance_size=self.instance_size, mode=self.mode)

    def run_algorithm(self):
        """ Overriding the abstract method
            Run other author algorithm, placed in codes directory (see below) """
        valid_ls = []
        equal_ls = []
        criteria_ls = []
        measures_ls = []
        algo_to_check = []
        errors_ls = []
        if self.last_names:
            algo_to_check = self.last_names
        elif self.last_name:
            algo_to_check = [self.last_name]
        elif self.code_path:
            algo_to_check = [self.code_path.split(".")[0]]
        if self.instance_size:
            instances_to_check = [self.instance_size]
        else:
            instances_to_check = list(range(50, 501, 50))
        for last_name_ in algo_to_check:
            last_name_data_check = "martsich"
            print("\n{:-^50}".format(last_name_.upper()))
            for instance_size in instances_to_check:
                print(CLIColors.BOLD + f"--- Processing {last_name_} code for instance of {instance_size}" + CLIColors.ENDC)
                start_time = time.time()
                result = (None, None, None)
                timestamp = None
                error = None
                try:
                    if os.path.isfile(f"codes/{last_name_}.py"):
                        python_command = "python" if sys.platform == "win32" else "python3"
                        res = check_output([python_command,
                                            f"codes/{last_name_}.py",
                                            f"data/in_{last_name_data_check}_{instance_size}.txt",
                                            f"data"])
                        # print(res.decode("utf-8"))

                    elif os.path.isfile(f"codes/{last_name_}.jar"):
                        res = check_output(["java",
                                            "-jar",
                                            f"codes/{last_name_}.jar",
                                            f"data/in_{last_name_data_check}_{instance_size}.txt",
                                            f"data/"])
                    else:
                        error = "No code file"
                    timestamp = time.time() - start_time
                    if not error:
                        result = run_validate(last_name=last_name_data_check,
                                              instance_size=instance_size,
                                              mode=self.mode)

                except Exception as exp:
                    error = exp
                if error:
                    print(CLIColors.FAIL + f"{last_name_}: {error}" + CLIColors.ENDC)
                valid_ls.append(result[0])
                equal_ls.append(result[1])
                criteria_ls.append(result[2].__str__().replace(".", ",") if result[2] else "")
                measures_ls.append(timestamp.__str__().replace(".", ","))
                errors_ls.append(error)
            clean_after(out_dir="data", last_name_to_clean=last_name_data_check)

        save_to_csv(last_names=algo_to_check, instances=instances_to_check, measures=measures_ls,
                    valid=valid_ls, equal=equal_ls, calculated=criteria_ls, errors=errors_ls)
        print(CLIColors.OKGREEN + f"--- Successfully finished!" + CLIColors.ENDC)


def clean_after(out_dir, last_name_to_clean):
    for instance_size in range(50, 501, 50):
        path = os.path.join(out_dir, f"out_{last_name_to_clean}_{instance_size}.txt")
        if os.path.isfile(path):
            os.remove(path)
    print(CLIColors.OKBLUE + f"--- Cleaned out instances for {last_name_to_clean}" + CLIColors.ENDC)


def save_to_csv(last_names, instances, measures, valid, equal, calculated, errors):
    result = []
    for l_idx, ln in enumerate(last_names):
        for inst_idx, inst in enumerate(instances):
            result.append([
                ln,
                inst,
                measures[l_idx * len(instances) + inst_idx],
                valid[l_idx * len(instances) + inst_idx],
                equal[l_idx * len(instances) + inst_idx],
                calculated[l_idx * len(instances) + inst_idx],
                errors[l_idx * len(instances) + inst_idx] or "",
            ])
    df = pd.DataFrame(data=result,
                      columns=["last name", 'instance size', 'time [s]', 'valid', 'correct', 'criteria', "errors"])
    filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".csv"
    path = os.path.join("test_results", filename)
    df.to_csv(path)
    print(CLIColors.OKGREEN + f"--- Result has been saved to the {path}" + CLIColors.ENDC)
    return


def main():
    cli = MyCLI()


if __name__ == '__main__':
    main()
