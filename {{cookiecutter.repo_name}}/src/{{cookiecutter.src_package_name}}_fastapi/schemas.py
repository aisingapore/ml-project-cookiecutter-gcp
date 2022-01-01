import typing
import pydantic


class Review(pydantic.BaseModel):
    id: int
    text: str


class MovieReviews(pydantic.BaseModel):
    reviews: typing.List[Review]
