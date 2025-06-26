import asyncio
import random
import time

async def continuous_event_feeder(queue, stop_event):
    """
    Producer that continuously fetches and puts events into the queue
    until a stop_event is set.
    """
    event_id = 0
    print("Continuous Event Feeder: Starting...")
    while not stop_event.is_set():
        await asyncio.sleep(random.uniform(0.2, 0.8)) # Simulate fetching an event
        event_id += 1
        event = f"Background-Event-{event_id}"
        await queue.put(event)
        print(f"Continuous Event Feeder: Put '{event}' into queue. (Queue size: {queue.qsize()})")
    print("Continuous Event Feeder: Stopping.")
    # Important: Put a None for EACH potential consumer that is still active
    # For a fixed number of consumers, put N Nones.
    # For dynamic consumers, a more sophisticated shutdown (e.g., using queue.join())
    # or a different sentinel mechanism might be needed.
    # In this example, we have 2 consumers, so we'll put 2 Nones.
    await queue.put(None)
    await queue.put(None)


class QueueAsyncIterator:
    """
    An asynchronous iterator wrapper for asyncio.Queue to allow async for.
    """
    def __init__(self, queue):
        self._queue = queue

    # FIX: __aiter__ should NOT be async def. It should just return self.
    def __aiter__(self):
        return self

    async def __anext__(self):
        item = await self._queue.get()
        # Ensure task_done is called for every item taken from the queue
        self._queue.task_done() # Call task_done for the item we just got

        if item is None:
            raise StopAsyncIteration
        return item

async def event_consumer_with_async_for(name, event_stream):
    """
    Consumer that processes events using async for from an event stream (AsyncIterator).
    """
    print(f"Consumer {name}: Starting to process events...")
    try:
        async for event in event_stream:
            print(f"Consumer {name}: Consumed and processing '{event}'")
            await asyncio.sleep(random.uniform(0.5, 1.5)) # Simulate processing time
            # Note: task_done() is now handled within __anext__ of QueueAsyncIterator
    except asyncio.CancelledError:
        print(f"Consumer {name}: Was cancelled.")
    except Exception as e:
        print(f"Consumer {name}: Encountered error: {e}")
    finally:
        print(f"Consumer {name}: Finished processing events.")


async def main_combined():
    queue = asyncio.Queue()
    stop_signal = asyncio.Event() # Event to signal the producer to stop

    # Start the continuous producer in the background
    producer_task = asyncio.create_task(continuous_event_feeder(queue, stop_signal))

    # Create an async iterator for the queue for each consumer
    # Each consumer needs its own "view" of the queue, or they will race for the 'None' sentinel.
    # If using a single QueueAsyncIterator for multiple consumers, only the first one
    # to hit 'None' will stop, the others will hang.
    # The common practice is either:
    # 1. Each consumer gets its own `QueueAsyncIterator` and the producer sends N `None`s.
    # 2. Consumers directly use `while True: item = await queue.get()` and handle `None`.
    # Let's stick with option 1 for demonstrating `async for`.
    event_stream_for_consumer1 = QueueAsyncIterator(queue)
    event_stream_for_consumer2 = QueueAsyncIterator(queue)

    # Start consumers that use async for
    consumer1_task = asyncio.create_task(event_consumer_with_async_for("C1", event_stream_for_consumer1))
    consumer2_task = asyncio.create_task(event_consumer_with_async_for("C2", event_stream_for_consumer2))


    # Let the system run for a while (e.g., 10 seconds)
    print("\n--- Running for 10 seconds ---")
    await asyncio.sleep(10) # Simulate application runtime

    # Signal the producer to stop
    print("\n--- Signalling producer to stop ---")
    stop_signal.set()
    await producer_task # Wait for the producer to actually finish and put Nones

    # Wait for all consumers to complete.
    # queue.join() could also be used here if you wanted to wait for the queue to be empty
    # after all items put by the producer (including Nones) have been processed.
    # But `asyncio.gather` on consumer tasks directly is good for awaiting their completion.
    await asyncio.gather(consumer1_task, consumer2_task)

    print("\n--- All tasks completed ---")
    print(f"Final queue size: {queue.qsize()}")


if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main_combined())
    end_time = time.perf_counter()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")
