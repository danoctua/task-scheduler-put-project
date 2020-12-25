from task_scheduler.task import Task


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

    def get_tasks(self, id_only=True):
        """
        Get all tasks this machine performs (ordered)
        :param id_only:
        :return:
        """
        if id_only:
            return [x.task_id for x in self.tasks]
        return self.tasks

    def get_time_over(self) -> float:
        """
        For mode 2 only: get time of processing for the last task
        :return: time in float
        """
        if not self.tasks:
            return 0
        return self.cur_time - self.tasks[-1].r_time

    def get_time_over_weighted(self) -> float:
        result = 0.0
        for task_nr, task in enumerate(self.tasks):
            result += (max(0, self.times_finished[task_nr] - task.d_time) * task.w)
        return result

    def get_due_time(self):
        ls = []
        for task_nr, task in enumerate(self.tasks):
            ls.append("{} {} {}".format(task.d_time, self.times_finished[task_nr],
                                       max(0, self.times_finished[task_nr] - task.d_time) * task.w))
        return ls
