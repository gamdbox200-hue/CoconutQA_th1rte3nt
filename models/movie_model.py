from pydantic import BaseModel
from typing import Optional


class GenreModel(BaseModel):
    name: str


class MovieModel(BaseModel):
    id: int
    name: str
    price: float
    description: str
    imageUrl: Optional[str] = None
    location: str
    published: bool
    genreId: int
    genre: GenreModel
    createdAt: str
    rating: float
    reviews: Optional[list] = None

    model_config = {"extra": "ignore"}


class MoviesListResponse(BaseModel):
    movies: list[MovieModel]
    count: int
    page: int
    pageSize: int
    pageCount: int

    model_config = {"extra": "ignore"}
