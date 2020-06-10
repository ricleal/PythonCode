# Python program creating a context manager
from contextlib import contextmanager


class MyContextManager1():
    def __init__(self):
        print('init method called')

    def __enter__(self):
        print('enter method called')
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('exit method called')


@contextmanager
def my_context_manager_2(task_name):
    print("Starting...", task_name)
    try:
        yield
    finally:
        print("Finishing...")


def main():
    with MyContextManager1():
        print("** with 1!")

    with my_context_manager_2("Context Manager 2"):
        print("** with 2!")

if __name__ == "__main__":
    main()
