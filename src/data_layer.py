import csv
import dataclasses
from decimal import Decimal
from src.models import CompanyData

COMPANY_DATA_KEY_MAPPING = {
    'company_name': 'Company Name',
    'industry': 'Industry',
    'market_capitalization': 'Market Capitalization',
    'revenue': 'Revenue (in millions)',
    'ebitda': 'EBITDA (in millions)',
    'net_income': 'Net Income (in millions)',
    'debt': 'Debt (in millions)',
    'equity': 'Equity (in millions)',
    'enterprise_value': 'Enterprise Value (in millions)',
    'pe_ratio': 'P/E Ratio',
    'revenue_growth_rate': 'Revenue Growth Rate (%)',
    'ebitda_margin': 'EBITDA Margin (%)',
    'net_income_margin': 'Net Income Margin (%)',
    'roe': 'ROE (Return on Equity) (%)',
    'roa': 'ROA (Return on Assets) (%)',
    'current_ratio': 'Current Ratio',
    'debt_to_equity_ratio': 'Debt to Equity Ratio',
    'location': 'Location',
    'ceo': 'CEO',
    'number_of_employees': 'Number of Employees'
}


def load_company_data(company_name: str) -> CompanyData | None:
    """
    Fetch stored company data matching company name. Return None if no match found.

    :param company_name: name of company
    :return: CompanyData object if found, otherwise None
    """
    with open('data/database.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Company Name'] == company_name:
                return parse_company_data(row)

    return None


def parse_company_data(company_data: dict) -> CompanyData:
    """
    Parse dict to CompanyData object.

    :param company_data: dict containing company data
    :return: CompanyData object
    """

    parsed_fields = {f.name: company_data.get(COMPANY_DATA_KEY_MAPPING[f.name]) for f in dataclasses.fields(CompanyData)}
    return CompanyData(**parsed_fields)
