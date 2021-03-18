import asyncio


class RequestHandler:
    __classname__: str = None

    async def handle_request(self, func: str, args: dict[str, object]) -> object:
        pass
