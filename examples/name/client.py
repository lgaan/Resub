import asyncio
from pubsub import Pub

pub = Pub()  # Initialise Pub with default params


async def main() -> None:
    """Send the user's name from an input."""
    while True:
        user_name = input("What is your name? ")

        await pub.send("name", user_name=user_name)  # Send the user's input via IPC to the other process

asyncio.run(main())  # Run the method
