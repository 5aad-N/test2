from typing import Any, TypedDict
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder


class ApiResponse(TypedDict, total=False):
    """Type definition for API responses"""
    success: bool
    data: dict[str, Any] | None
    error: str | None
    errors: dict[str, list[str]] | None


def json_response(
    data: dict[str, Any] | None = None,
    error: str | None = None,
    errors: dict[str, list[str]] | None = None,
    status: int = 200
) -> JsonResponse:
    """
    Standardized JSON response format for API endpoints.

    Args:
        data: Success response data
        error: Single error message string
        errors: Dictionary of field-level errors
        status: HTTP status code

    Returns:
        JsonResponse with standardized format
    """
    response: ApiResponse = {"success": error is None and errors is None}

    if data is not None:
        response["data"] = data
    if error is not None:
        response["error"] = error
    if errors is not None:
        response["errors"] = errors

    return JsonResponse(response, status=status, encoder=DjangoJSONEncoder)
