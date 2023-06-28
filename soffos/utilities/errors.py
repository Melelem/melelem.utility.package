class ErrorResponse:
    def __init__(
        self, 
        service: str, 
        details: str = None, 
        message: str = None, 
        status_code: int = 400
        ) -> None:
        self.service = service
        self.details = details
        self.message = message
        self.status_code = status_code

    def to_dict(self, exclude_empty: bool = False):
        if exclude_empty:
            return {k: v for k, v in vars(self).items() if v is not None}
        return vars(self)
        