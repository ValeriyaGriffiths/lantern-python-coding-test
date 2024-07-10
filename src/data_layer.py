import csv
import dataclasses
from decimal import Decimal
from models import CompanyData

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
    with open('../data/database.csv', newline='') as csvfile:
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

    parsed_fields = {}
    for f in dataclasses.fields(CompanyData):
        field_value = company_data.get(COMPANY_DATA_KEY_MAPPING[f.name])
        parsed_fields[f.name] = Decimal(field_value) if field_value and f.type == Decimal else field_value

    return CompanyData(**parsed_fields)

    # return CompanyData(company_name=company_data['Company Name'],
    #                    industry=company_data['Industry'],
    #                    market_capitalization=Decimal(company_data['Market Capitalization']),
    #                    revenue=company_data['Revenue (in millions)'],
    #                    ebitda=company_data['EBITDA (in millions)'],
    #                    net_income=company_data['Net Income (in millions)'],
    #                    debt=company_data['Debt (in millions)'],
    #                    equity=company_data['Equity (in millions)'],
    #                    enterprise_value=company_data['Enterprise Value (in millions)'],
    #                    pe_ratio=company_data['P/E Ratio'],
    #                    revenue_growth_rate=company_data['Revenue Growth Rate (%)'],
    #                    ebitda_margin=company_data['EBITDA Margin (%)'],
    #                    net_income_margin=company_data['Net Income Margin (%)'],
    #                    roe=company_data['ROE (Return on Equity) (%)'],
    #                    roa=company_data['ROA (Return on Assets) (%)'],
    #                    current_ratio=company_data['Current Ratio'],
    #                    debt_to_equity_ratio=company_data['Debt to Equity Ratio'],
    #                    location=company_data['Location'],
    #                    ceo=company_data['CEO'],
    #                    number_of_employees=company_data['Number of Employees']
    #                    )
