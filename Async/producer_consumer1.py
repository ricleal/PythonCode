import asyncio
import random
import time

async def event_producer_generator(num_batches=5, events_per_batch=3):
    """
    An asynchronous generator that yields events.
    Simulates fetching events from an external source over time.
    """
    print("Event Producer: Starting to fetch events...")
    for batch in range(1, num_batches + 1):
        await asyncio.sleep(random.uniform(0.5, 1.5)) # Simulate delay in fetching a batch
        print(f"Event Producer: Fetched Batch {batch}")
        for i in range(1, events_per_batch + 1):
            event = f"Event-{batch}-{i}"
            print(f"Event Producer: Yielding '{event}'")
            yield event
            await asyncio.sleep(random.uniform(0.1, 0.3)) # Simulate delay between yielding events within a batch

    print("Event Producer: Finished yielding all events.")

async def event_processor():
    """
    Asynchronous function that processes events using async for.
    """
    print("Event Processor: Starting to process events...")
    async for event in event_producer_generator():
        print(f"Event Processor: Consumed and processing '{event}'")
        await asyncio.sleep(random.uniform(0.5, 1.0)) # Simulate event processing time
    print("Event Processor: All events processed.")

async def main():
    """
    Main asynchronous function to run the event processor.
    """
    start_time = time.perf_counter()
    await event_processor() # Simply await the event processor to complete
    end_time = time.perf_counter()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
