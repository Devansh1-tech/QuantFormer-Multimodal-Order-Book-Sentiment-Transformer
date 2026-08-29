"""
===========================================================
QuantFormer Backend — Common Schemas
===========================================================

Standardized response wrappers and error schemas used
across all API endpoints for consistent JSON structure.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

from typing import Any, Optional

from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    """
    Standard wrapper for all successful API responses.
    """

    success: bool = Field(default=True, description="Whether the request succeeded")
    message: str = Field(default="OK", description="Human-readable status message")
    data: Optional[Any] = Field(default=None, description="Response payload")
    timestamp: str = Field(description="ISO 8601 timestamp of the response")


class ErrorResponse(BaseModel):
    """
    Standard wrapper for all error responses.
    """

    success: bool = Field(default=False)
    error: str = Field(description="Error type or code")
    message: str = Field(description="Human-readable error message")
    detail: Optional[str] = Field(default=None, description="Additional debug context")
    timestamp: str = Field(description="ISO 8601 timestamp of the error")


class RootResponse(BaseModel):
    """
    Response schema for the root GET / endpoint.
    """

    project: str = Field(description="Project name")
    description: str = Field(description="Project description")
    version: str = Field(description="Application version")
    status: str = Field(description="Current status")
    documentation: str = Field(description="API docs URL")
    endpoints: dict = Field(description="Available API endpoint summary")
