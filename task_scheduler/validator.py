from task_scheduler.machine import Machine


class Validator:

    def __init__(self, tasks: list, order: str = "", separator=" ", machines=None, mode=1):
        """

        :param tasks: list of tasks type of task_scheduler.Task
        :type tasks: list(task_scheduler.Task)
        :param order: 
        :param separator:
        :param machines:
        :param mode:
        """
        if machines is None:
            machines = []
        self.tasks: list = tasks
        self.value = 0
        self.mode: int = mode
        self.order: list = []
        self.machines = machines
        self.instance_size = None
        if self.mode in (1, 3):
            order_split = order.split(separator)
            for idx in order_split:
                if idx.isdigit():
                    self.order.append(int(idx))
            self.instance_size = len(self.order)
        elif self.mode == 2:
            ls_order = order.split("\n")
            if not self.machines or len(self.machines) != len(ls_order):
                if len(ls_order) > len(self.machines):
                    ls_order = ls_order[:len(self.machines)]
                else:
                    raise AttributeError("[ERROR] validator.py - Wrong machines list length. Try again")
            for line in ls_order:
                tmp = []
                for idx in line.split(separator):
                    if idx.isdigit():
                        tmp.append(int(idx))
                self.order.append(tmp)
            self.instance_size = sum([len(x) for x in self.order])

    def show_description(self):
        """
        Show description of current order
        :return:
        """
        if self.mode != 1:
            print("Implemented only for the first mode.")
            return
        result = []
        cur_time = 0
        for idx in self.order:
            task = self.tasks[idx-1]
            cur_time = max(task.r_time + task.p_time, cur_time + task.p_time)
            result.append(f"[#{task.r_time}..{cur_time - task.p_time}..{task.w}..{cur_time}..{task.d_time}]")
        print(" ".join(result))

    def calculate(self):
        """
        Calculate criteria for current data set
        :return: calculated value of criteria (int or float depends on the mode)
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
            for machine_idx, machine_queue in enumerate(self.order):
                cur_time = 0
                for task_id in machine_queue:
                    task = self.tasks[task_id - 1]
                    cur_time = max(task.r_time + task.p_time * self.machines[machine_idx].speed,
                                   cur_time + task.p_time * self.machines[machine_idx].speed)
                    result += (cur_time - task.r_time)
            result /= self.instance_size
        elif self.mode == 3:
            for machine_id, machine in enumerate(self.machines):
                if not isinstance(machine, Machine):
                    pass
                for order_id, task_id in enumerate(self.order):
                    task = self.tasks[task_id - 1]
                    if machine_id == 0:
                        machine.add_task(
                            task,
                            p_time=task.p_times[machine_id]
                        )
                    else:
                        machine.add_task(
                            task=task,
                            min_start_time=self.machines[machine_id-1].get_time_available(order_id),
                            p_time=task.p_times[machine_id]
                        )
                    result += max(0, machine.get_time_available() - task.d_time) * task.w
            result /= sum(x.w for x in self.tasks)
        return round(result, 2)

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
