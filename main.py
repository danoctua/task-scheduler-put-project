from task_generator import Generator
import os

cur_dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    generator = Generator("data")
    for instances in range(50, 501, 50):
        generator.run(instances)
