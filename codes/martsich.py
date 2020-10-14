import sys
import os


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
        print("Wrong instances count")
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

        # This part of code below is LICENCED so you can't copy it into the project...

        def get_next(cur_tasks, cur_time):
            if len(cur_tasks) < 1:
                return None, []
            cur_tasks = list(sorted(cur_tasks, key=lambda x: (x.d_time - x.p_time < cur_time, x.r_time)))
            # print(cur_time, cur_tasks[0], [x.__str__() for x in cur_tasks[1:]])
            return cur_tasks[0], cur_tasks[1:]

        next_task, tasks = get_next(cur_tasks=self.tasks, cur_time=self.cur_time)
        self.cur_time += (next_task.p_time + next_task.r_time)
        tasks_sorted = [next_task]
        while next_task:
            next_task, tasks = get_next(cur_tasks=tasks, cur_time=self.cur_time)
            if not next_task:
                continue
            self.cur_time = max(self.cur_time + next_task.p_time, next_task.p_time + next_task.r_time)
            if next_task.d_time < self.cur_time:
                self.result += next_task.w
            tasks_sorted.append(next_task)
        self.order = [task.task_id for task in tasks_sorted]
        return self.order

    def save_to_file(self, file_path):
        with open(file_path, "w") as file:
            result = f"{self.result}\n"
            result += " ".join([str(x) for x in self.order])
            file.write(result)


if __name__ == '__main__':
    path_file = os.path.join("data", sys.argv[-1])
    if os.path.exists(path_file):
        with open(path_file, "r") as file:
            tasks = upload_tasks(file.read())
        engine = Engine(tasks=tasks, instance_size=len(tasks))
        engine.run()
        engine.save_to_file(path_file.replace("in", "out"))
        print(f"Processed for instance from {path_file}")
    else:
        print("File doesn't exists")
