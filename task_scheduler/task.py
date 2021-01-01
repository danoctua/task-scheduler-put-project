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
        input_str = input_str.strip()
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
