import sys
import os
import collections


class Task:

    task_id = None
    p_time = None
    r_time = None
    d_time = None
    w = None

    def __init__(self, *args):
        """
        :param task_id: Task id
        :param p_time: processing time
        :param r_time: ready time
        :param d_time: due time
        :param w: weight of task
        """
        if len(args) > 2:

            self.task_id = args[0]
            self.p_time = args[1]
            self.r_time = args[2]
            if len(args) > 3:
                self.d_time = args[3]
                if len(args) > 4:
                    self.w = args[4]

    def parse_input(self, task_id, input_str, separator=" ", to_int=True):
        params = input_str.split(separator)
        if len(params) < 2:
            raise AttributeError("Not enough parameters in line")
        if to_int:
            for idx, item in enumerate(params):
                params[idx] = int(item)
        self.task_id = task_id
        self.p_time = params[0]
        self.r_time = params[1]
        if len(params) > 2:
            self.d_time = params[2]
            if len(params) > 3:
                self.w = params[3]
        return

    def __str__(self, separator: str = " ", idx_include: bool = False):
        if idx_include:
            result = f"{self.task_id}" + separator
        else:
            result = ""
        result += f"{separator}".join([str(x) for x in [self.p_time, self.r_time]])
        if self.d_time:
            result += (f"{separator}" + str(self.d_time))
        if self.w:
            result += (f"{separator}" + str(self.w))
        return result


class Machine:
    machine_id: int = None
    cur_time: int = None
    speed: float = None
    tasks: list = None

    def __init__(self, machine_id: int, speed: float = 1.0):
        self.machine_id = machine_id
        self.cur_time = 0
        self.speed = speed
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.cur_time = max(self.cur_time + self.speed * task.p_time, task.r_time + self.speed * task.p_time)

    def get_time_available(self):
        return self.cur_time

    def check_time_ready(self, task: Task):
        return max(self.cur_time + self.speed * task.p_time, task.r_time + self.speed * task.p_time)

    def get_tasks(self, id_only=True):
        if id_only:
            return [x.task_id for x in self.tasks]
        return self.tasks

    def get_time_over(self):
        if not self.tasks:
            return 0
        return self.cur_time - self.tasks[-1].r_time


def upload_tasks(input_str: str, separator: str = " ", mode: int = 1) -> (list, list):
    """
    Parse text input and create lists of tasks and machines
    :param input_str: raw text
    :param separator: column separator
    :param mode: 1 - one machine + p|r|d|w, 2 - multiple machines + p|r
    :return: tuple of tasks and engines
    """
    lines = input_str.split("\n")
    tasks = []
    machines = []
    start_tasks = 1
    n = lines[0]
    try:
        n = int(n)
    except ValueError:
        print(n)
        AttributeError("Wrong instances amount")
    if mode == 2:
        start_tasks = 2
        if lines[1]:
            tmp = lines[1].split(separator)
            for idx, i in enumerate(tmp):
                fl_i = float(i)
                machines.append(Machine(machine_id=idx, speed=fl_i))
        else:
            AttributeError("No machines speeds")
    lines = lines[start_tasks:]
    for idx in range(1, n+1):
        new_task = Task()
        new_task.parse_input(idx, lines[idx-1])
        tasks.append(new_task)
    return tasks, machines


class Engine:

    def __init__(self, tasks, machines=None, mode=1):
        self.tasks = tasks
        if mode == 2 and not machines:
            raise AttributeError("[ERROR] engine.py - For the mode 2 you have to provide machines speeds")
        self.mode = mode
        self.machines = machines

        self.instance_size = len(tasks)
        self.cur_time = 0
        self.order = []
        self.result = 0

    def run(self) -> list:

        self.result = 0

        # This part of code below is LICENCED so you can't copy it into the project...

        def get_next_one_machine(cur_tasks: list, to_pass: list, cur_time: int):
            """
            Get next task to schedule from task list for the mode 1
            :param cur_tasks: list of Task objects to schedule
            :param to_pass: list of tasks to pass (append to this list new tasks to pass and return)
            :param cur_time: current time after scheduling previous tasks
            :return: tuple : [0] - next task, [1] - list of tasks to schedule,
                                [2] - list of tasks to pass and append to the end
            """
            if len(cur_tasks) < 1:
                return None, [], to_pass

            idx = 0
            found = False
            for idx, task in enumerate(cur_tasks):
                if task.too_late(cur_time):
                    to_pass.append(task)
                    self.result += task.w
                    continue
                else:
                    found = True
                    break
            if found:
                return cur_tasks[idx], cur_tasks[idx + 1:], to_pass
            else:
                return None, [], to_pass

        def get_machine_best_choice(task: Task) -> Machine:
            machines = list(sorted(self.machines, key=lambda x: x.check_time_ready(task)))
            return machines[0]

        if self.mode == 1:

            # sort by a) due time, b) weight (desc)
            tasks = list(sorted(self.tasks, key=lambda x: (x.d_time, -x.w)))

            next_task, tasks, passed_tasks = get_next_one_machine(cur_tasks=tasks, to_pass=[], cur_time=self.cur_time)
            self.cur_time += (next_task.p_time + next_task.r_time)
            tasks_scheduled = [next_task]
            while next_task:
                next_task, tasks, passed_tasks = get_next_one_machine(cur_tasks=tasks, to_pass=passed_tasks, cur_time=self.cur_time)
                # if no task - end loop
                if not next_task:
                    continue
                # set current time after scheduling task
                self.cur_time = max(self.cur_time + next_task.p_time, next_task.p_time + next_task.r_time)
                tasks_scheduled.append(next_task)

            tasks_scheduled += passed_tasks

            self.order = [task.task_id for task in tasks_scheduled]
        elif self.mode == 2:
            tasks = list(sorted(self.tasks, key=lambda x: x.r_time))
            for task in tasks:
                machine = get_machine_best_choice(task)
                machine.add_task(task)
                self.result += machine.get_time_over()
            for machine in self.machines:
                self.order.append(machine.get_tasks(id_only=True))
            self.result = round(self.result/self.instance_size, 2)
            # -- generating test output
            # self.order = [list() for _ in range(len(self.machines))]
            # for task in self.tasks:
            #     self.order[(task.task_id - 1) % len(self.machines)].append(task.task_id)

        return self.order

    def save_to_file(self, file_path):
        with open(file_path, "w") as file:
            result = f"{self.result}\n"
            if self.mode == 1:
                result += " ".join([str(x) for x in self.order])
            elif self.mode == 2:
                result += "\n".join([" ".join([str(x) for x in y]) for y in self.order])
            file.write(result)


def task_scheduling():
    path_file = sys.argv[-2]
    save_dir = sys.argv[-1]
    if os.path.exists(path_file):
        with open(path_file, "r") as file:
            tasks, machines = upload_tasks(file.read(), mode=2)
        filename = os.path.split(path_file)[-1]
        engine = Engine(tasks=tasks, machines=machines, mode=2)
        engine.run()
        engine.save_to_file(os.path.join(save_dir, filename.replace("in", "out")))
        print(f"Processed for instance from {path_file}")
    else:
        print(path_file)
        print("Input instance file doesn't exists")


if __name__ == '__main__':
    task_scheduling()
