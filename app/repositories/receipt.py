from sqlalchemy import select, or_

from app.models import Receipt, ReceiptCompound, Category
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
    receipt = Receipt
    receipt_compound = ReceiptCompound
    category = Category
    async def known_categories(self, user_id: int, names: list[str], exclude_category_id: int) -> dict[str, int]:
        stmt = (
            select(self.receipt_compound.name, self.receipt_compound.category_id)
            .where(
                or_(
                    self.receipt_compound.user_id == ADMIN_USER_ID,
                    self.receipt_compound.user_id == user_id
                ),
                self.receipt_compound.name.in_(names),
                self.receipt_compound.category_id != exclude_category_id,
            )
            .order_by(self.receipt_compound.id)
        )
        result = await self.session.execute(stmt)
        return {name: group_id for name, group_id in result}

    async def get_receipts_compound(self, user_id: int, limit: int, offset: int) -> list[dict]:
        stmt = (
            select(
                self.receipt.period,
                self.receipt_compound.name,
                self.category.name.label("group_name"),
                self.receipt_compound.vat,
                self.receipt_compound.vat_sum,
                self.receipt_compound.price,
                self.receipt_compound.quantity,
                self.receipt_compound.sum
            )
            .join(self.receipt, self.receipt_compound.receipt_id == self.receipt.id)
            .join(self.category, self.receipt_compound.category_id == self.category.id)
            .where(self.receipt_compound.user_id == user_id)
            .order_by(self.receipt_compound.id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return [dict(row) for row in result.mappings()]


    # period: datetime
    # name: str
    # group_name: str
    # vat: int
    # vat_sum: float
    # price: float
    # quantity: float
    # sum: float

