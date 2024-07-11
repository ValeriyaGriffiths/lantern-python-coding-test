import dataclasses
import json
from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass
class CompanyData:
    """
    Assumes net_income_margin, ceo, number_of_employees to be optional based on provided data.
    """

    company_name: str
    industry: str
    market_capitalization: Decimal
    revenue: Decimal
    ebitda: Decimal
    net_income: Decimal
    debt: Decimal
    equity: Decimal
    enterprise_value: Decimal
    pe_ratio: Decimal
    revenue_growth_rate: Decimal
    ebitda_margin: Decimal
    net_income_margin: Decimal | None
    roe: Decimal
    roa: Decimal
    current_ratio: Decimal
    debt_to_equity_ratio: Decimal
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


@dataclass
class DataDiscrepancyCheckerResponse:
    uploaded_data: CompanyData
    stored_data: CompanyData
    mismatched_fields: list[MismatchedFields]

    def to_json(self):
        return json.dumps(dataclasses.asdict(self))

    def __eq__(self, other):
        """
        Workaround for comparison failing for objects with identical attribute values.
        FIXME - this works but I am not sure why it was failing in the first place.
        """
        return vars(self) == vars(other)
