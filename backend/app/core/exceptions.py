from fastapi import Request, status
from fastapi.responses import JSONResponse
from backend.app.core.logging_config import error_logger

class QuantFormerException(Exception):
    """Base exception for all QuantFormer custom exceptions."""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ModelNotReadyException(QuantFormerException):
    def __init__(self, model_name: str):
        super().__init__(
            message=f"Model '{model_name}' is not ready or failed to load.",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )

class MarketDataException(QuantFormerException):
    def __init__(self, message: str):
        super().__init__(
            message=f"Market Data Error: {message}",
            status_code=status.HTTP_400_BAD_REQUEST
        )

class NewsFetchException(QuantFormerException):
    def __init__(self, message: str):
        super().__init__(
            message=f"News Fetch Error: {message}",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )

async def quantformer_exception_handler(request: Request, exc: QuantFormerException):
    error_logger.error(f"QuantFormerException: {exc.message} | URL: {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "status": "error"}
    )

async def global_exception_handler(request: Request, exc: Exception):
    error_logger.error(f"Unhandled Exception: {str(exc)} | URL: {request.url}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "An unexpected internal server error occurred.", "status": "error"}
    )
