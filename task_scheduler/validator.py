class Validator:

    def __init__(self, tasks: list, order: str = "", separator=" "):
        self.tasks = tasks
        self.value = 0
        order_split = order.split(separator)
        self.order = []
        for idx in order_split:
            self.order.append(int(idx))

    def calculate(self) -> int:
        cur_time = 0
        result = 0
        for task_id in self.order:
            task = self.tasks[task_id-1]
            cur_time = max(task.r_time + task.p_time, cur_time + task.p_time)
            if cur_time > task.d_time:
                result += task.w
            # print(cur_time, task, result)
        self.value = result
        return result

    def validate(self, value: int):
        result = self.calculate()
        return result == value and len(set(self.order)) == len(self.order), result

