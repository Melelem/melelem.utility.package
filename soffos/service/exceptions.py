from typing import Any

class ServiceException(Exception):
    def __init__(
        self,
        service: str,
        status_code: int,
        message: str, 
        details: Any = None
        ) -> None:
        self.service = service
        self.status_code = status_code
        self.message = message
        self.details = details
        
    def to_response(self):
        return {k: v for k, v in vars(self).items() if k != 'status_code'}

class BadRequestException(ServiceException):
    def __init__(self, service: str, message: str, details: str = None):
        super().__init__(service=service, status_code=400, message=message, details=details)

class InternalServerErrorException(ServiceException):
    def __init__(self, service: str, message: str, details: str = None):
        super().__init__(service=service, status_code=500, message=message, details=details)
