class DataRepositoryError(Exception):
    def __init__(self, message: str):
        self.message = message


class DataNotFoundError(DataRepositoryError):
    pass


class UpdateOperationFailed(DataRepositoryError):
    pass
