from sqlalchemy import select, or_
from collections.abc import Sequence

from app.models import Category
from app.repositories.base import BaseRepository
from app.constants import ADMIN_USER_ID


class CategoryRepository(BaseRepository[Category]):
    model = Category

    async def get_by_name(self, name: str) -> Category | None:
        stmt = select(self.model).where(self.model.name == name)
        return await self.session.scalar(stmt)

    async def list_for_user(self, user_id: int) -> Sequence[Category]:
        stmt = select(self.model).where(
            or_(self.model.user_id == user_id,
                self.model.user_id == ADMIN_USER_ID,)
        ).order_by(self.model.id)
        result = await self.session.scalars(stmt)
        return result.all()