from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProviderProduct(Base):
    __tablename__ = "provider_products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    provider_id: Mapped[int] = mapped_column(
        ForeignKey("providers.id"),
        nullable=False,
        index=True,
    )

    provider_product_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    product_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )