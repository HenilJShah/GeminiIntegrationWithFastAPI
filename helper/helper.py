from typing import Any

from models.paper_model import StandardResponse


class DBUri:
    """
    Contains the MongoDB connection URI.

    Attributes:
        MONGO_DB_URI (str): The URI for connecting to the MongoDB database.
    """

    MONGO_DB_URI = "mongodb://localhost:27017/"


class CustomStandard:
    """
    Provides a standardized response structure for API responses.
    """

    @staticmethod
    def response(code: int, status: str, message: str, data: Any = None) -> dict:
        """
        Creates a standardized response dictionary using the StandardResponse model.

        Args:
            code (int): The response code indicating the result of the operation (e.g., 200 for success, 404 for not found).
            status (str): The status of the response (e.g., "success" or "error").
            message (str): A descriptive message providing additional details about the response.
            data (Any, optional): The data payload to include in the response. Defaults to None.

        Returns:
            dict: A dictionary representation of the standardized response, containing the fields 'code', 'status', 'message', and 'data'.
        """
        return StandardResponse(
            code=code, status=status, message=message, data=data
        ).model_dump()
