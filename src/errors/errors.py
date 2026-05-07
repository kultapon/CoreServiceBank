from fastapi import status


class AppError(Exception):

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str):
        self.detail = detail


class ForbiddenError(AppError):
    status_code = status.HTTP_403_FORBIDDEN


class UniqueConstraintError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND


class TokenError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED


class DatabaseError(AppError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR