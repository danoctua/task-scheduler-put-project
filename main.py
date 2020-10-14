from task_generator import Generator

if __name__ == '__main__':
    generator = Generator("data")
    for instances in range(50, 501, 50):
        generator.run(instances)
