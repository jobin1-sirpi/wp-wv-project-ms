from typing import Dict, List, Literal, TypedDict
from pydantic import BaseModel


class AuthorizationData(TypedDict):
    access_token: str
    email: str


class SuccessfulResponse(BaseModel):
    success: bool = True
    status_code: Literal[200]
    message: str = "This is initial route of WP-WV-PROJECT-MS"
    data: None
    error: None
    meta: None


class CreatedResponse(BaseModel):
    success: bool = True
    status_code: Literal[201]
    message: str = "Created"
    data: None
    error: None
    meta: None


class UnauthorizedErrorResponse(BaseModel):
    success: bool = False
    status_code: Literal[401]
    message: str = "Unauthorized"
    data: None
    error: Dict[str, str] = {
        "code": "UNAUTHORIZED",
        "details": "Authentication required",
    }
    meta: None


class ForbiddenErrorResponse(BaseModel):
    success: bool = False
    status_code: Literal[403]
    message: str = "Forbidden"
    data: None
    error: Dict[str, str] = {
        "code": "FORBIDDEN",
        "details": "You are not authorized to access this resource.",
    }
    meta: None


class NotFoundErrorResponse(BaseModel):
    success: bool = False
    status_code: Literal[404]
    message: str = "Not Found"
    data: None
    error: Dict[str, str] = {
        "code": "NOT_FOUND",
        "details": "The requested resource could not be found.",
    }
    meta: None


class ConflictErrorResponse(BaseModel):
    success: bool = False
    status_code: Literal[409]
    message: str = "Conflict Error"
    data: None
    error: Dict[str, str] = {
        "code": "CONFLICT_ERROR",
        "details": "The resource you are trying to access is already in use.",
    }
    meta: None


class ValidationErrorDetails(BaseModel):
    field: str
    error: str


class ValidationErrorError(BaseModel):
    code: Literal["VALIDATION_ERROR"]
    details: List[ValidationErrorDetails]


class ValidationErrorResponse(BaseModel):
    success: bool = False
    status_code: Literal[422]
    message: Literal["Validation Error"]
    data: None
    error: ValidationErrorError
    meta: None


class TooManyRequestsError(BaseModel):
    success: bool = False
    status_code: Literal[429]
    message: str = "Too Many Requests"
    data: None
    error: Dict[str, str] = {
        "code": "TOO_MANY_REQUESTS",
        "details": "Rate limit exceeded. Try again later.",
    }
    meta: None


class BackendError(BaseModel):
    code: Literal["INTERNAL_SERVER_ERROR"]
    details: Literal[
        "Something went wrong. Please contact developers if issue persists."
    ]


class BackendErrorResponse(BaseModel):
    success: bool = False
    status_code: Literal[500]
    message: str = "Internal Server Error"
    data: None
    error: BackendError
    meta: None


HOME_RESPONSE_MODEL = {
    200: {"model": SuccessfulResponse},
    500: {"model": BackendErrorResponse},
}
