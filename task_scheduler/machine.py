from task_scheduler.task import Task


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
