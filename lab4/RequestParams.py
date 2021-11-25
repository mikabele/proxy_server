class RequestParams:
    __handler: str = None
    __func: str = None
    __args: dict[str, str] = None

    def __init__(self, handler: str, func: str = None, args: dict[str, str] = None):
        if args is None:
            args = {}
        self.__handler = handler
        self.__func = func
        self.__args = args

    def get_handler(self) -> str:
        return self.__handler

    def get_func(self) -> str:
        return self.__func

    def get_args(self) -> dict[str, str]:
        return self.__args
