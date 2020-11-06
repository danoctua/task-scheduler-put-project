class Task:

    task_id = None
    p_time = None
    r_time = None
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

            self.task_id = args[0]
            self.p_time = args[1]
            self.r_time = args[2]
            if len(args) > 3:
                self.d_time = args[3]
                if len(args) > 4:
                    self.w = args[4]

    def parse_input(self, task_id, input_str, separator=" ", to_int=True):
        params = input_str.split(separator)
        if len(params) < 2:
            raise AttributeError("Not enough parameters in line")
        if to_int:
            for idx, item in enumerate(params):
                params[idx] = int(item)
        self.task_id = task_id
        self.p_time = params[0]
        self.r_time = params[1]
        if len(params) > 2:
            self.d_time = params[2]
            if len(params) > 3:
                self.w = params[3]
        return

    def __str__(self, separator: str = " ", idx_include: bool = False):
        if idx_include:
            result = f"{self.task_id}" + separator
        else:
            result = ""
        result += f"{separator}".join([str(x) for x in [self.p_time, self.r_time]])
        if self.d_time:
            result += (f"{separator}" + str(self.d_time))
        if self.w:
            result += (f"{separator}" + str(self.w))
        return result
