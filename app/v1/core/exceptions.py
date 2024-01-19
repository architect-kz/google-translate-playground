class GoogleTranslateRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)


class WordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)


class WordInsertionException(Exception):
    def __init__(self, message):
        super().__init__(message)
