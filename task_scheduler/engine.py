from task_scheduler.task import Task
import sys
import os


def upload_tasks(input_str: str, separator: str = " ", mode: int = 1) -> (list, list):
    lines = input_str.split("\n")
    result = []
    engines = []
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
            for i in tmp:
                fl_i = float(i)
                engines.append(fl_i)
        else:
            AttributeError("No engines speeds")
    lines = lines[start_tasks:]
    for idx in range(1, n+1):
        new_task = Task()
        new_task.parse_input(idx, lines[idx-1])
        result.append(new_task)
    return result, engines


class Engine:

    def __init__(self, tasks, engines=None, mode=1):
        self.tasks = tasks
        if mode == 2 and not engines:
            raise AttributeError("[ERROR] engine.py - For the mode 2 you have to provide engines speeds")
        self.mode = mode
        self.engines = engines

        self.instance_size = len(tasks)
        self.cur_time = 0
        self.order = []
        self.result = 0

    def run(self) -> list:

        # This part of code below is LICENCED so you can't copy it into the project...

        def get_next_one_machine(cur_tasks, cur_time):
            if len(cur_tasks) < 1:
                return None, []
            cur_tasks = list(sorted(cur_tasks, key=lambda x: (x.d_time - x.p_time < cur_time, x.r_time)))
            # print(cur_time, cur_tasks[0], [x.__str__() for x in cur_tasks[1:]])
            return cur_tasks[0], cur_tasks[1:]
        if self.mode == 1:
            next_task, tasks = get_next_one_machine(cur_tasks=self.tasks, cur_time=self.cur_time)
            self.cur_time += (next_task.p_time + next_task.r_time)
            tasks_sorted = [next_task]
            while next_task:
                next_task, tasks = get_next_one_machine(cur_tasks=tasks, cur_time=self.cur_time)
                if not next_task:
                    continue
                self.cur_time = max(self.cur_time + next_task.p_time, next_task.p_time + next_task.r_time)
                if next_task.d_time < self.cur_time:
                    self.result += next_task.w
                tasks_sorted.append(next_task)
            self.order = [task.task_id for task in tasks_sorted]
        elif self.mode == 2:
            self.order = [list() for _ in range(len(self.engines))]
            for task in self.tasks:
                self.order[(task.task_id - 1) % len(self.engines)].append(task.task_id)
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
