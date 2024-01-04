
from fastapi import HTTPException


class ServerErrorException(HTTPException):
    """Server error exception."""

    def __init__(self, status_code=500, detail="Server error") -> None:
        """Init."""
        super().__init__(
            status_code=status_code,
            detail=detail,
        )


__all__ = ["ServerErrorException"]
