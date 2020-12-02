from task_scheduler.task import Task
import random
import os


class Generator:

    def __init__(self, dir_path, last_name, mode=1, machines_number=1):
        """
        :param dir_path: Directory path where to store your test data
        """
        self.dir_path = dir_path
        self.machines = [1.0]
        self.tasks = []
        self.last_name = last_name
        self.n = 0
        self.mode = mode
        density_coof = 2
        self.density = 1 if self.mode in [1, 3] else machines_number // density_coof
        self.machines_number = machines_number

    def run(self, n: int):
        self.n = n
        self.tasks = []
        self.machines = [1.0]
        avr_time = 6
        delta = 4
        p_time = 0
        p_times = []
        r_time = 0
        if self.mode == 2:
            for x in range(self.machines_number - 1):
                self.machines.append(max(1.0, round(random.uniform(1, 3), 2)))
                random.shuffle(self.machines)
        for idx in range(1, n + 1):
            if self.mode in (1, 2):
                p_time = max(avr_time + random.randint(-delta, delta), 1)
                r_time = max(idx * avr_time // self.density + random.randint(-avr_time // self.density * delta, 0), 0)
            else:
                p_times = []
                for i in range(3):
                    p_times.append(max(avr_time + random.randint(-delta, delta), 1))
            if self.mode in (1, 3):
                d_time = max(r_time + p_time, idx * avr_time + random.randint(0, avr_time * delta))
                w = random.randint(1, 6)
            else:
                (d_time, w) = (None, None)
            if self.mode in (1, 2):
                new_task = Task(idx, p_time, r_time, d_time, w)
            elif self.mode in (3,):
                new_task = Task(idx, *p_times, d_time, w)
            else:
                new_task = Task()
            self.tasks.append(new_task)
        random.shuffle(self.tasks)
        print(f"Generated {self.n} instances")

    def write_to_file(self):
        if not os.path.isdir(self.dir_path):
            print(f"No such directory: {self.dir_path}. Creating...")
            os.mkdir(self.dir_path)
            print(f"Directory {self.dir_path} has been created")
        result = [f"{self.n}"]
        if self.mode == 2:
            result.append(" ".join([str(x) for x in self.machines]))
        for task in self.tasks:
            result.append(str(task))
        with open(os.path.join(self.dir_path, f"in_{self.last_name}_{self.n}.txt"), "w") as file:
            file.write("\n".join(result))

    def to_order(self) -> str:
        result = "0\n"
        tasks = list(sorted(self.tasks, key=lambda x: x.task_id))
        if self.mode == 1:
            result += " ".join([str(x.task_id) for x in tasks])
        elif self.mode == 2:
            order_ls = []
            for x in range(self.machines_number - 1):
                tmp = []
                for y in range(len(tasks)//self.machines_number):
                    tmp.append(tasks[x * self.machines_number + y])
                order_ls.append(" ".join([str(x.task_id) for x in tmp]))
            result += "\n".join(order_ls)
        return result


if __name__ == '__main__':
    generator = Generator("data", "martsich")
    generator.run(50)
