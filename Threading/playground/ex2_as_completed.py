import concurrent.futures
import time


def task(name, duration):
    print(f"Task {name}: Starting (duration: {duration}s)")
    time.sleep(duration)
    print(f"Task {name}: Finished")
    return f"Result from {name}"


if __name__ == "__main__":
    print("Submitting tasks and processing results as they complete:")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        futures.append(executor.submit(task, "A", 3))
        futures.append(executor.submit(task, "B", 1))
        futures.append(executor.submit(task, "C", 2))

        print("\nProcessing results as they complete:")
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(f"Received: {result}")
            except Exception as exc:
                print(f"Task generated an exception: {exc}")

    print("\nUsing executor.map to submit tasks and retrieve results in order:")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for result in executor.map(task, ["A", "B", "C"], [3, 1, 2]):
            print(f"Received: {result}")
