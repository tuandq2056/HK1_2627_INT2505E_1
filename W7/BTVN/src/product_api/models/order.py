from datetime import datetime

from sqlalchemy import (
    CheckConstraint, DateTime, ForeignKey, Integer, String, UniqueConstraint,
    func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False)

    # 1 Order — N OrderItem; xoá order thì xoá luôn item
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="OrderItem.id",
    )

    @property
    def total_cents(self):
        return sum(i.line_total_cents for i in self.items)

    def __repr__(self):
        return f"<Order {self.id} {self.customer}>"


class OrderItem(db.Model):
    """Bảng nối Order ⟷ Product: một order có nhiều product, mỗi dòng có qty riêng."""

    __tablename__ = "order_items"
    __table_args__ = (
        UniqueConstraint("order_id", "product_id",
                         name="uq_order_items_order_product"),
        CheckConstraint("qty > 0", name="ck_order_items_qty_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), index=True, nullable=False)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), index=True, nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    # Chụp lại giá lúc đặt — đổi giá product sau này không ảnh hưởng order cũ
    unit_price_cents: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()  # noqa: F821

    @property
    def line_total_cents(self):
        return self.qty * self.unit_price_cents

    def __repr__(self):
        return f"<OrderItem order={self.order_id} product={self.product_id} qty={self.qty}>"
