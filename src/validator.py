"""
Validation module for construction change orders.

Uses Pydantic for structured data validation
and additional business rules for financial consistency.
"""

from typing import Optional, Union
from pydantic import BaseModel, Field, ConfigDict


class ExtractedField(BaseModel):
    """Structure for an individual extracted field."""

    model_config = ConfigDict(extra="forbid")

    value: Optional[Union[str, float]] = None

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    evidence: Optional[str] = None


class ChangeOrderResult(BaseModel):
    """Validated construction change-order information."""

    model_config = ConfigDict(extra="forbid")

    change_order_number: ExtractedField
    project_name: ExtractedField
    contractor: ExtractedField
    change_date: ExtractedField
    change_description: ExtractedField

    change_amount: ExtractedField
    original_contract_amount: ExtractedField
    revised_contract_amount: ExtractedField


def validate_extraction(data: dict) -> dict:
    """
    Validate extracted fields and apply financial
    consistency checks.
    """

    validated = ChangeOrderResult.model_validate(data)

    result = validated.model_dump()

    warnings = []

    # Check missing fields.
    for field_name, field_data in result.items():

        if field_data["value"] is None:

            warnings.append(
                f"Missing field: {field_name}"
            )

    # Retrieve financial values.
    original = result["original_contract_amount"]["value"]

    change = result["change_amount"]["value"]

    revised = result["revised_contract_amount"]["value"]

    # Validate contract calculations.
    financial_values = [original, change, revised]

    if all(
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        for value in financial_values
    ):

        expected_amount = original + change

        if abs(expected_amount - revised) > 0.01:

            warnings.append(
                "Financial inconsistency: original contract "
                "amount plus change amount does not equal "
                "the revised contract amount."
            )

    else:

        warnings.append(
            "Financial consistency could not be checked "
            "because one or more monetary values are missing."
        )

    result["validation_warnings"] = warnings

    result["validation_status"] = (
        "passed" if not warnings else "review_required"
    )

    return result
