from typing import Any
from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"
    RESPONSE_MODEL = ErrorResponse

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(
            status_code=self.STATUS_CODE,
            detail=self.DETAIL,
            **kwargs
        )
        
    def __class_getitem__(cls, _):
        return cls