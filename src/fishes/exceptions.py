from fastapi import status

from src.exceptions import DetailedHTTPException


class FishNotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Fish not found"


class FishRegionAlreadyExists(DetailedHTTPException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "This fish is already assigned to this region"


class DuplicateScientificName(DetailedHTTPException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "Fish with this scientific name already exists"


class FishRegionNotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Fish is not assigned to this region"