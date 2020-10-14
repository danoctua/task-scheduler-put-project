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
