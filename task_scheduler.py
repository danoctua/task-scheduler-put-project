from main import *


def parse_argv(argv):
    last_name = None
    action = None
    try:
        last_name_idx = argv.index("--who")
        try:
            last_name = argv[last_name_idx + 1]
            run_validate(last_name)
        except:
            pass
    except:
        pass
    return action, last_name


if __name__ == '__main__':
    parse_argv(sys.argv[1:])
