from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Optional
from pydantic import BaseModel, Field


class CompanyData(BaseModel):
    """
    Assumes net_income_margin, ceo, number_of_employees to be optional based on provided data.
    """
    company_name: str = Field(alias="Company Name")
    industry: str = Field(alias="Industry")
    market_capitalization: Decimal = Field(alias="Market Capitalization")
    revenue: Decimal = Field(alias="Revenue (in millions)")
    ebitda: Decimal = Field(alias="EBITDA (in millions)")
    net_income: Decimal = Field(alias="Net Income (in millions)")
    debt: Decimal = Field(alias="Debt (in millions)")
    equity: Decimal = Field(alias="Equity (in millions)")
    enterprise_value: Decimal = Field(alias="Enterprise Value (in millions)")
    pe_ratio: Decimal = Field(alias="P/E Ratio")
    revenue_growth_rate: Decimal = Field(alias="Revenue Growth Rate (%)")
    ebitda_margin: Decimal = Field(alias="EBITDA Margin (%)")
    net_income_margin: Optional[Decimal] = Field(None, alias="Net Income Margin (%)")
    roe: Decimal = Field(alias="ROE (Return on Equity) (%)")
    roa: Decimal = Field(alias="ROA (Return on Assets) (%)")
    current_ratio: Optional[Decimal] = Field(None, alias="Current Ratio")
    debt_to_equity_ratio: Decimal = Field(alias="Debt to Equity Ratio")
    location: str = Field(alias="Location")
    ceo: Optional[str] = Field(None, alias="CEO")
    number_of_employees: Optional[int] = Field(None, alias="Number of Employees")


class MismatchedFields(BaseModel):
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
