import asyncio

import aioredis
import aioredis.abc


class Sub:
    def __init__(
        self,
        address: str = "redis://localhost",
        channel: str = "ipc:1",
        loop: asyncio.AbstractEventLoop = None
    ):
        self.loop = loop or asyncio.get_event_loop()

        self.address = address
        self.channel_address = channel
        self.channel = None

        self.redis_connection = None
        self.task = None

        self.endpoints = {}

    @staticmethod
    def listener(name: str = None) -> callable:
        def wrapper(func):
            func.__redis_sub_route__ = name or func.__name__

            return func

        return wrapper

    def route(self, name: str = None):
        def wrapper(func):
            self.endpoints[name or func.__name__] = func

            return func

        return wrapper

    def register(self, cls) -> None:
        for method in dir(cls):
            method = getattr(cls, method)

            try:
                self.endpoints[method.__redis_sub_route__] = method
            except AttributeError:
                continue

    async def prepare(self) -> None:
        self.redis_connection = await aioredis.create_redis(
            self.address
        )

        self.channel = (await self.redis_connection.subscribe(self.channel_address))[0]

    async def __consumer(self, channel: aioredis.abc.AbcChannel) -> None:
        while True:
            while await channel.wait_message():
                message = await channel.get_json()
                endpoint = message.get("endpoint")

                if endpoint in self.endpoints:
                    await self.endpoints[endpoint](**message.get("data"))

    async def start(self) -> None:
        if not self.redis_connection:
            await self.prepare()

        self.task = asyncio.create_task(self.__consumer(self.channel))
        await self.task
