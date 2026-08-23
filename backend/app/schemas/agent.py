from pydantic import BaseModel, ConfigDict, Field, field_validator


class GroceryItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    quantity: float
    unit: str = Field(min_length=1)

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Quantity must be greater than 0")

        return value


class GroceryRequirements(BaseModel):
    model_config = ConfigDict(extra="forbid")

    people: int
    days: int
    diet: str | None
    budget: float | None
    items: list[GroceryItem] = Field(min_length=1)

    @field_validator("people", "days")
    @classmethod
    def validate_positive_integer(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Value must be greater than 0")

        return value

    @field_validator("budget")
    @classmethod
    def validate_budget(
        cls,
        value: float | None,
    ) -> float | None:
        if value is not None and value < 0:
            raise ValueError("Budget cannot be negative")

        return value