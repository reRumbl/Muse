from pydantic import BaseModel


class SuccessResponse(BaseModel):
    message: str


class CountResponse(BaseModel):
    count: int
