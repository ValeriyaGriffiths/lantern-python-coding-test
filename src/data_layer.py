import csv
from src.models import CompanyData
from src.config import settings


def load_company_data(company_name: str) -> CompanyData | None:
    """
    Fetch stored company data matching company name. Return None if no match found.

    :param company_name: name of company
    :return: CompanyData object if found, otherwise None
    """

    with open(settings.db_location, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Company Name'] == company_name:
                return CompanyData(**row)

    return None


def parse_company_data(company_data: dict) -> CompanyData:
    """
    Parse dict to CompanyData object.

    :param company_data: dict containing company data
    :return: CompanyData object
    """

    return CompanyData(**company_data)
