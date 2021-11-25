from lab4.RequestResult import RequestResult


class RequestHandler:
    __classname__: str = None

    async def handle_request(self, func: str, args: dict[str, str]) -> RequestResult:
        pass

    def get_classname(self) -> str:
        pass
