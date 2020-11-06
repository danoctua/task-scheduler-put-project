import sys
import os
import collections


class Task:

    def __init__(self, *args):
        """
        :param task_id: Task id
        :param p_time: processing time
        :param r_time: ready time
        :param d_time: due time
        :param w: weight of task
        """
        if len(args) >= 4:

            self.task_id = args[0]
            self.p_time = args[1]
            self.r_time = args[2]
            self.d_time = args[3]
            self.w = args[4]

    def parse_input(self, task_id, input_str, separator=" ", to_int=True):
        params = input_str.split(separator)
        if len(params) < 4:
            raise AttributeError("Not enough parameters in line")
        if to_int:
            for idx, item in enumerate(params):
                params[idx] = int(item)
        self.task_id = task_id
        self.p_time = params[0]
        self.r_time = params[1]
        self.d_time = params[2]
        self.w = params[3]
        return

    def too_late(self, start):
        return self.p_time + start > self.d_time

    def __str__(self, separator: str = " ", idx_include: bool = False):
        if idx_include:
            result = f"{self.task_id}" + separator
        else:
            result = ""
        return result + f"{self.p_time}{separator}{self.r_time}{separator}{self.d_time}{separator}{self.w}"


def upload_tasks(input_str: str) -> list:
    lines = input_str.split("\n")
    result = []
    n = lines[0]
    try:
        n = int(n)
    except ValueError:
        print("Wrong instances number")
        return result
    for idx in range(1, n+1):
        new_task = Task()
        new_task.parse_input(idx, lines[idx])
        result.append(new_task)
    return result


class Engine:

    def __init__(self, tasks, instance_size=0):
        self.tasks = tasks
        self.cur_time = 0
        self.order = []
        self.instance_size = instance_size
        self.result = 0

    def run(self) -> list:

        # This part of code below is LICENCED so you can't copy it into your project...

        # sort by a) due time, b) weight (desc)
        tasks = list(sorted(self.tasks, key=lambda x: (x.d_time, -x.w)))

        def get_next(cur_tasks: list, to_pass: list, cur_time: int):
            """
            Get next task to schedule from task list
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
                return cur_tasks[idx], cur_tasks[idx+1:], to_pass
            else:
                return None, [], to_pass

        next_task, tasks, passed_tasks = get_next(cur_tasks=tasks, to_pass=[], cur_time=self.cur_time)
        self.cur_time += (next_task.p_time + next_task.r_time)
        tasks_scheduled = [next_task]
        while next_task:
            next_task, tasks, passed_tasks = get_next(cur_tasks=tasks, to_pass=passed_tasks, cur_time=self.cur_time)
            # if no task - end loop
            if not next_task:
                continue
            # set current time after scheduling task
            self.cur_time = max(self.cur_time + next_task.p_time, next_task.p_time + next_task.r_time)
            tasks_scheduled.append(next_task)

        tasks_scheduled += passed_tasks

        self.order = [task.task_id for task in tasks_scheduled]
        return self.order

    def save_to_file(self, file_path):
        with open(file_path, "w") as file:
            result = f"{self.result}\n" + " ".join([str(x) for x in self.order])
            file.write(result)


def task_scheduling():
    path_file = sys.argv[-2]
    save_dir = sys.argv[-1]
    if os.path.exists(path_file):
        with open(path_file, "r") as file:
            tasks = upload_tasks(file.read())
        filename = os.path.split(path_file)[-1]
        engine = Engine(tasks=tasks, instance_size=len(tasks))
        engine.run()
        engine.save_to_file(os.path.join(save_dir, filename.replace("in", "out")))
        print(f"Processed for instance from {path_file}")
    else:
        print(path_file)
        print("Input instance file doesn't exists")


if __name__ == '__main__':
    task_scheduling()
