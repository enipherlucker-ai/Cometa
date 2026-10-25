from pydantic import BaseModel


class ItemCategory(BaseModel):
    index: int
    category_id: int


class Categorization(BaseModel):
    items: list[ItemCategory]