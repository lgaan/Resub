import asyncio
from pubsub import Sub


sub = Sub()  # Initialise Sub with default params


@sub.route()
async def name(user_name: str) -> None:
    print("User input: ", user_name)  # Print out the input received via IPC.


asyncio.run(sub.start())  # Start the IPC server.
