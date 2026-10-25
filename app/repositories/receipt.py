from sqlalchemy import select, or_

from app.models import Receipt, ReceiptCompound
from app.repositories.base import BaseRepository
from app.constants import ADMIN_USER_ID


class ReceiptRepository(BaseRepository[Receipt]):
    model = Receipt

    async def get_by_qrraw(self, user_id: int, qrraw: str) -> Receipt | None:
        stmt = select(self.model).where(
            or_(
                self.model.user_id == ADMIN_USER_ID,
                self.model.user_id == user_id
            ),
            self.model.qrraw == qrraw)
        return await self.session.scalar(stmt)


class ReceiptCompoundRepository(BaseRepository[ReceiptCompound]):
    model = ReceiptCompound
    async def known_categories(self, user_id: int, names: list[str], exclude_category_id: int) -> dict[str, int]:
        stmt = (
            select(self.model.name, self.model.category_id)
            .where(
                or_(
                    self.model.user_id == ADMIN_USER_ID,
                    self.model.user_id == user_id
                ),
                self.model.name.in_(names),
                self.model.category_id != exclude_category_id,
            )
            .order_by(self.model.id)
        )
        result = await self.session.execute(stmt)
        return {name: group_id for name, group_id in result}
