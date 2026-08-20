from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    canonical_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    brand: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    quantity_value: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 3),
        nullable=True,
    )

    quantity_unit: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )