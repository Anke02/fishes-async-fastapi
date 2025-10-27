from src.exceptions import DetailedHTTPException
from fastapi import status


class RegionNotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Region not found"


class RegionAlreadyExists(DetailedHTTPException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "Region with this name already exists"


class RegionInUse(DetailedHTTPException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "Region cannot be deleted because it is assigned to some fishes"