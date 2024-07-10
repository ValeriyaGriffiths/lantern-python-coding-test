import csv
from models import CompanyData


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
    # TODO convert decimals

    return CompanyData(company_name=company_data['Company Name'],
                       industry=company_data['Industry'],
                       market_capitalization=company_data['Market Capitalization'],
                       revenue=company_data['Revenue (in millions)'],
                       ebitda=company_data['EBITDA (in millions)'],
                       net_income=company_data['Net Income (in millions)'],
                       debt=company_data['Debt (in millions)'],
                       equity=company_data['Equity (in millions)'],
                       enterprise_value=company_data['Enterprise Value (in millions)'],
                       pe_ratio=company_data['P/E Ratio'],
                       revenue_growth_rate=company_data['Revenue Growth Rate (%)'],
                       ebitda_margin=company_data['EBITDA Margin (%)'],
                       net_income_margin=company_data['Net Income Margin (%)'],
                       roe=company_data['ROE (Return on Equity) (%)'],
                       roa=company_data['ROA (Return on Assets) (%)'],
                       current_ratio=company_data['Current Ratio'],
                       debt_to_equity_ratio=company_data['Debt to Equity Ratio'],
                       location=company_data['Location']
                       )

