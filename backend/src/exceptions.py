from fastapi import HTTPException, status


class ForbiddenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have permission to access this resource'
        )
