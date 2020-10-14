from task import Task
import random
import os

last_name = "martsich"


class Generator:

    def __init__(self, dir_path):
        """

        :param dir_path: Directory path where to store your test data
        """
        self.dir_path = dir_path
        if not os.path.isdir(dir_path):
            print(f"No such directory: {dir_path}. Creating...")
            os.mkdir(dir_path)
            print(f"Directory {dir_path} has been created")
        self.tasks = []
        self.n = 0

    def run(self, n: int):
        self.n = n
        self.tasks = []
        avr_time = 4
        for idx in range(1, n+1):
            p_time = max(avr_time + random.randint(-2, 2), 1)
            r_time = max(idx * avr_time + random.randint(-avr_time, 0), 0)
            d_time = max(r_time + p_time, idx * avr_time + random.randint(0, avr_time))
            w = random.randint(1, 6)
            new_task = Task(idx, p_time, r_time, d_time, w)
            self.tasks.append(new_task)
        random.shuffle(self.tasks)
        self.write_to_file()
        print(f"Generated {self.n} instances")

    def write_to_file(self):
        result = [f"{self.n}"]
        for task in self.tasks:
            result.append(str(task))
        with open(os.path.join(self.dir_path, f"in_{last_name}_{self.n}.txt"), "w") as file:
            file.write("\n".join(result))


if __name__ == '__main__':
    generator = Generator("")
    generator.run(50)
