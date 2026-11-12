import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger("rumbo.errors")

class AppError(Exception):
    status_code: int = 400
    code :str = "APP_ERROR"

    def __init__(self, message:str) -> None:
        super().__init__(message)
        self.message = message

class NotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"

class ConflictError(AppError):
    status_code = 409
    code = "CONFLICT"

class UnauthorizedError(AppError):
    status_code = 401
    code = "UNAUTHORIZED"

class ForbiddenError(AppError):
    status_code = 403
    code = "FORBIDEN"

def _error_body(request: Request, code:str, message:str)-> dict:
    return{
        "error":{
            "code": code,
            "message": message,
            "request_id": getattr(request.state, "request_id", None)
        }
    }

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request:Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content=_error_body(request, exc.code, exc.message)
        )

    @app.exception_handler(RequestValidationError)
    async def   handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        body = _error_body(request, "VALIDATION_ERROR", "Invalid request data")
        body["error"]["details"] = jsonable_encoder(exc.errors())
        return JSONResponse(status_code=422, content=body)

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        logger.exception("Unhandled error request id =%s", request_id)
        return JSONResponse(
            status_code=500, content=_error_body(request, "INTERNAL_ERROR", "Unexpected error")
        )