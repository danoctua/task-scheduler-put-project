class Validator:

    def __init__(self, tasks: list, order: str = "", separator=" ", engines=None, mode=1):
        if engines is None:
            engines = []
        self.tasks: list = tasks
        self.value = 0
        self.mode: int = mode
        self.order: list = []
        self.engines = engines
        if self.mode == 1:
            order_split = order.split(separator)
            for idx in order_split:
                if idx.isdigit():
                    self.order.append(int(idx))
        elif self.mode == 2:
            ls_order = order.splitlines()
            if not self.engines or len(self.engines) != len(ls_order):
                raise AttributeError("[ERROR] validator.py - Wrong engines list length. Try again")
            for line in ls_order:
                tmp = []
                for idx in line.split(separator):
                    if idx.isdigit():
                        tmp.append(int(idx))
                self.order.append(tmp)

    def show_description(self):
        if self.mode != 1:
            print("Implemented only for the first mode and debug.")
            return
        result = []
        cur_time = 0
        for idx in self.order:
            task = self.tasks[idx-1]
            cur_time = max(task.r_time + task.p_time, cur_time + task.p_time)
            result.append(f"[#{task.r_time}..{cur_time - task.p_time}..{task.w}..{cur_time}..{task.d_time}]")
        print(" ".join(result))

    def calculate(self) -> int:
        """

        :return: calculated value of criteria
        """
        cur_time = 0
        result = 0

        if self.mode == 1:
            for task_id in self.order:
                task = self.tasks[task_id-1]
                cur_time = max(task.r_time + task.p_time, cur_time + task.p_time)
                if cur_time > task.d_time:
                    result += task.w
                # print(cur_time, task, result)
            self.value = result
        elif self.mode == 2:
            for engine_queue in self.order:
                for task_id in engine_queue:
                    task = self.tasks[task_id - 1]
                    cur_time = max(task.r_time + task.p_time, cur_time + task.p_time)
                    result += (cur_time - task.r_time)
        return result

    def validate(self, value: int) -> tuple:
        """

        :param value: validate calculated value with provided one
        :return: tuple: is format valid, is calculated value equal to value in the file, calculated value
        """
        result = self.calculate()
        flat_order = flat_list(self.order)
        return len(set(flat_order)) == len(flat_order), result == value, result


def flat_list(obj, full_list=[]) -> list:
    if not isinstance(obj, list):
        return full_list + [obj]
    for x in obj:
        full_list = flat_list(x, full_list)
    return full_list
