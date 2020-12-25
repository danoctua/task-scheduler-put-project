import sys
import os


class Task:

    task_id = None
    p_time = None
    p_times = None
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
            self.parse_input(task_id=int(args[0]), input_str=" ".join([str(x) for x in args[1:] if x is not None]))

    def parse_input(self, task_id=0, input_str=None, separator=" ", to_int=True) -> None:
        """
        Parse task from string
        :param task_id:
        :type task_id: int
        :param input_str: input string which contains separated task attributes
        :param separator: input_str separator
        :param to_int: convert attributes to int
        :return:
        """
        if not input_str:
            return
        params = input_str.split(separator)
        if len(params) < 2:
            raise AttributeError("Not enough parameters in line")
        if to_int:
            for idx, item in enumerate(params):
                params[idx] = int(item)
        self.task_id = task_id
        if len(params) > 4:
            # for mode 3
            self.p_times = params[:3]
        else:
            self.p_time = params[0]
            self.r_time = params[1]
        if len(params) > 3:
            # for mode 1
            self.d_time = params[-2]
            self.w = params[-1]
        elif len(params) > 2:
            # for mode 2 without weight
            self.d_time = params[-1]

    def too_late(self, cur_time) -> bool:
        return cur_time > self.d_time

    def __str__(self, separator: str = " ", idx_include: bool = False):
        if idx_include:
            result = f"{self.task_id}" + separator
        else:
            result = ""
        result += f"{separator}".join([str(x) for x in [self.p_time,
                                                        " ".join([str(x) for x in self.p_times]) if self.p_times else None,
                                                        self.r_time] if x])
        if self.d_time:
            result += (f"{separator}" + str(self.d_time))
        if self.w:
            result += (f"{separator}" + str(self.w))
        return result



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
    if mode == 3:
        for idx in range(3):
            machines.append(Machine(machine_id=idx))
    lines = lines[start_tasks:]
    for idx in range(1, n+1):
        new_task = Task()
        new_task.parse_input(idx, lines[idx-1])
        tasks.append(new_task)
    return tasks, machines


class Machine:
    machine_id: int = None
    cur_time = None
    speed: float = None
    tasks: list = None
    times_finished: list = None

    def __init__(self, machine_id: int, speed: float = 1.0):
        self.machine_id = machine_id
        self.cur_time = 0
        self.speed = speed
        self.tasks = []
        self.times_finished = []

    def add_task(self, task: Task, min_start_time=None, p_time=None):
        """
        Add task to current machine
        :param task:
        :param min_start_time: for the mode 3 - provide minimal possible time of performing
                (end of performing on the previous machine)
        :param p_time: for the mode 3 - provide task p_time for this machine
        :return:
        """
        if p_time is None:
            p_time = task.p_time
            if p_time is None:
                raise AttributeError("Processing time hasn't been provided")
        self.cur_time = self.check_time_ready(task, min_start_time, p_time)
        self.tasks.append(task)

        self.times_finished.append(self.cur_time)

    def get_time_available(self, order_task_id: int = None):
        if order_task_id is None:
            return self.cur_time
        elif order_task_id >= len(self.tasks):
            raise IndexError("Tasks list contains less items, than you want to check")
        else:
            return self.times_finished[order_task_id]

    def check_time_ready(self, task: Task, min_start_time=None, p_time=None):
        """
        Check minimal task ready time without submitting task
        :param task:
        :param min_start_time: for the mode 3 - provide minimal possible time of performing
                (end of performing on the previous machine)
        :param p_time: for the mode 3 - provide task p_time for this machine
        :return: time
        """
        if min_start_time is None:
            min_start_time = 0
        if p_time is None:
            p_time = task.p_time
            if p_time is None:
                raise AttributeError("Processing time hasn't been provided")
        return max(x for x in [self.cur_time, task.r_time, min_start_time] if x is not None) + self.speed * p_time

    def get_time_over_weighted(self) -> float:
        result = 0.0
        for task_nr, task in enumerate(self.tasks):
            result += (max(0, self.times_finished[task_nr] - task.d_time) * task.w)
        return result


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

        if self.mode == 3:
            self.order = []
            tasks_sorted = sorted(self.tasks, key=lambda x: (x.d_time, -x.w))
            while tasks_sorted:
                task = self.get_flow_shop_best_choice(tasks_sorted)
                # task = tasks_sorted[0]
                tasks_sorted.remove(task)
                self.order.append(task.task_id)
                for machine_id, machine in enumerate(self.machines):
                    machine.add_task(
                        task,
                        p_time=task.p_times[machine_id],
                        min_start_time=self.machines[machine_id - 1].get_time_available() if machine_id else 0)
            result = self.machines[-1].get_time_over_weighted()
            result /= sum(task.w for task in self.tasks)
            self.result = round(result, 2)
        return self.order

    def get_flow_shop_best_choice(self, tasks: list) -> Task:
        times = []
        times_ready = [[] for _ in range(len(self.machines))]
        for task_nr in range(0, min(len(tasks), 10)):
            task = tasks[task_nr]
            time = 0
            for machine_idx, machine in enumerate(self.machines):
                time = machine.check_time_ready(
                    p_time=task.p_times[machine_idx],
                    task=task,
                    min_start_time=times_ready[machine_idx-1][task_nr] if machine_idx > 0 else 0
                )
                times_ready[machine_idx].append(time)
            times.append((task, (time - task.d_time) * task.w))
        chosen: Task = max(times, key=lambda x: (x[1], x[0].w))[0]
        return chosen

    def save_to_file(self, file_path):
        with open(file_path, "w") as file:
            result = f"{self.result}\n"
            if self.mode in (1, 3):
                result += " ".join([str(x) for x in self.order])
            elif self.mode == 2:
                result += "\n".join([" ".join([str(x) for x in y]) for y in self.order])
            file.write(result)


def task_scheduling():
    path_file = sys.argv[-2]
    save_dir = sys.argv[-1]
    if os.path.exists(path_file):
        with open(path_file, "r") as file:
            tasks, machines = upload_tasks(file.read(), mode=3)
        filename = os.path.split(path_file)[-1]
        engine = Engine(tasks=tasks, machines=machines, mode=3)
        engine.run()
        engine.save_to_file(os.path.join(save_dir, filename.replace("in", "out")))
        print(f"Processed for instance from {path_file}")
    else:
        print(path_file)
        print("Input instance file doesn't exists")


if __name__ == '__main__':
    task_scheduling()
