from task_scheduler.task import Task
from task_scheduler.machine import Machine
import sys
import os


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
            best_machine = min(self.machines, key=lambda x:  x.check_time_ready(task))
            return best_machine

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


if __name__ == '__main__':
    path_file = sys.argv[-1]
    if os.path.exists(path_file):
        with open(path_file, "r") as file:
            tasks_uploaded = upload_tasks(file.read())
        engine = Engine(tasks=tasks_uploaded)
        engine.run()
        engine.save_to_file(path_file.replace("in", "out"))
        print(f"Processed for instance from {path_file}")
