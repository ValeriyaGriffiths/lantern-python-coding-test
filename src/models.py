import dataclasses
import json
from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass
class CompanyData:
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
    net_income_margin: Decimal
    roe: Decimal
    roa: Decimal
    current_ratio: Decimal
    debt_to_equity_ratio: Decimal
    location: str
    ceo: str
    number_of_employees: int

    # def to_json(self):
    #     return json.dumps(dataclasses.asdict(self))

    def __eq__(self, other):
        """
        Workaround for comparison failing for objects with identical attribute values.
        FIXME - this works but I am not sure why it was failing in the first place.
        """
        return vars(self) == vars(other)


@dataclass
class DataDifference:
    field_name: str
    uploaded_value: Any
    stored_value: Any

    # def to_json(self):
    #     return json.dumps(dataclasses.asdict(self))


@dataclass
class ValidatorResponse:
    uploaded_data: CompanyData
    stored_data: CompanyData
    data_difference: list[DataDifference]

    def to_json(self):
        return json.dumps(dataclasses.asdict(self))

