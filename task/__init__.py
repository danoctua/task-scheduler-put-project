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

    def parse_input(self, input_str, separator=" ", to_int=True):
        params = input_str.split(separator)
        if len(params) < 5:
            raise AttributeError("Not enough parameters in line")
        if to_int:
            for idx, item in enumerate(params):
                params[idx] = int(item)
        self.task_id = params[0]
        self.p_time = params[1]
        self.r_time = params[2]
        self.d_time = params[3]
        self.w = params[4]
        return

    def __str__(self, separator: str = " ", idx_include: bool = False):
        if idx_include:
            result = f"{self.task_id}" + separator
        else:
            result = ""
        return result + f"{self.p_time}{separator}{self.r_time}{separator}{self.d_time}{separator}{self.w}"
