from task_scheduler.task import Task
import random
import os


class Generator:

    def __init__(self, dir_path, last_name, mode=1, engines_number=1):
        """
        :param dir_path: Directory path where to store your test data
        """
        self.dir_path = dir_path
        if not os.path.isdir(dir_path):
            print(f"No such directory: {dir_path}. Creating...")
            os.mkdir(dir_path)
            print(f"Directory {dir_path} has been created")
        self.engines = [1.0]
        self.tasks = []
        self.last_name = last_name
        self.n = 0
        self.mode = mode
        self.engines_number = engines_number

    def run(self, n: int):
        self.n = n
        self.tasks = []
        self.engines = [1.0]
        avr_time = 4
        delta = 4
        if self.mode == 2:
            for x in range(self.engines_number - 1):
                self.engines.append(max(1.0, round(random.random() * 3, 2)))
        for idx in range(1, n + 1):
            p_time = max(avr_time + random.randint(-delta, delta), 1)
            r_time = max(idx * avr_time + random.randint(-avr_time * delta, 0), 0)
            if self.mode == 1:
                d_time = max(r_time + p_time, idx * avr_time + random.randint(0, avr_time * delta))
                w = random.randint(1, 6)
            else:
                (d_time, w) = (None, None)
            new_task = Task(idx, p_time, r_time, d_time, w)
            self.tasks.append(new_task)
        random.shuffle(self.tasks)
        self.write_to_file()
        print(f"Generated {self.n} instances")

    def write_to_file(self):
        result = [f"{self.n}"]
        if self.mode == 2:
            result.append(" ".join([str(x) for x in self.engines]))
        for task in self.tasks:
            result.append(str(task))
        with open(os.path.join(self.dir_path, f"in_{self.last_name}_{self.n}.txt"), "w") as file:
            file.write("\n".join(result))


if __name__ == '__main__':
    generator = Generator("data", "martsich")
    generator.run(50)
