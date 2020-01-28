
class CannotGetMarketInfo(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)

class WrongWebSocketMessage(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)