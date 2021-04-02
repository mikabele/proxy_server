class RequestResult(object):
    __result: object = None

    def __init__(self, result: object):
        self.__result = result

    def __str__(self):
        return str(self.__result)
