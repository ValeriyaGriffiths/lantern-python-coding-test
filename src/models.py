from dataclasses import dataclass
from typing import Any
from pydantic import BaseModel

@dataclass
class CompanyData:
    """
    Assumes net_income_margin, ceo, number_of_employees to be optional based on provided data.
    """

    company_name: str
    industry: str
    market_capitalization: float
    revenue: float
    ebitda: float
    net_income: float
    debt: float
    equity: float
    enterprise_value: float
    pe_ratio: float
    revenue_growth_rate: float
    ebitda_margin: float
    net_income_margin: float | None
    roe: float
    roa: float
    current_ratio: float
    debt_to_equity_ratio: float
    location: str
    ceo: str | None
    number_of_employees: int | None

    def __eq__(self, other):
        """
        Workaround for comparison failing for objects with identical attribute values.
        FIXME - this works but I am not sure why it was failing in the first place.
        """
        return vars(self) == vars(other)


@dataclass
class MismatchedFields:
    field_name: str
    uploaded_value: Any
    stored_value: Any

    def __eq__(self, other):
        """
        Workaround for comparison failing for objects with identical attribute values.
        FIXME - this works but I am not sure why it was failing in the first place.
        """
        return vars(self) == vars(other)


class DataDiscrepancyCheckerResponse(BaseModel):
    uploaded_data: CompanyData
    stored_data: CompanyData
    mismatched_fields: list[MismatchedFields]

    def __eq__(self, other):
        """
        Workaround for comparison failing for objects with identical attribute values.
        FIXME - this works but I am not sure why it was failing in the first place.
        """
        return vars(self) == vars(other)
