import asyncio

import aioredis
import aioredis.abc


class Pub:
    def __init__(
        self,
        address: str = "redis://localhost",
        channel: str = "ipc:1",
        loop=None
    ):
        self.loop = loop or asyncio.get_event_loop()

        self.address = address
        self.channel = channel

        self.redis_connection = None

    async def prepare(self) -> None:
        self.redis_connection = await aioredis.create_redis(
            self.address
        )

    async def send(self, endpoint: str, **kwargs) -> None:
        if not self.redis_connection:
            await self.prepare()

        fmt = {
            "endpoint": endpoint,
            "data": kwargs
        }

        await self.redis_connection.publish_json(
            self.channel,
            fmt
        )
