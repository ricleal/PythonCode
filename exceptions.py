import random

def f1():
    try:
        # 1/0
        {}['key']
    except ZeroDivisionError:
        print("division by zero error")
    except Exception:
        print("Unknown error")
        raise


def f2():

    class MyException(Exception):
        def __init__(self, message="Custom message"):
            self.message = message
            super().__init__(self.message)

        def __str__(self):
            return f'Error: {self.message}'

    def sometimes_raise_exception():
        n = random.choice(range(2))
        if n == 0:
            print(f"sometimes_raise_exception raised exception. n={n}")
            raise MyException()

    RETRIES = 5
    current_retry = 0
    while current_retry < RETRIES:
        try:
            sometimes_raise_exception()
        except MyException as err:
            if 'Custom message' in str(err):
                print(f"Expected exception. Retrying {current_retry} of {RETRIES}")
            else:
                print("Error: An unidentified error ocurred {current_retry} of {RETRIES}")
                return {}
        else:
            break
        current_retry += 1
        if current_retry == RETRIES:
            print("Error max retries {current_retry} of {RETRIES}")
            return {}
    return {"end": "success"}

print(f2())