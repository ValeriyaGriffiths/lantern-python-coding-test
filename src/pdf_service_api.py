from src.pdf_service import PdfService
from src.data_layer import parse_company_data
from src.models import CompanyData


COMPANY_NAME_FILE_PATH_MAPPING = {
    "HealthInc": "assets/healthinc.pdf",
    "RetailCo": "assets/retailco.pdf",
    "FinanceLLC": "assets/financellc.pdf",
}


def extract_and_parse_pdf_data(company_name: str, pdf_file) -> CompanyData:
    """
    Calls PdfService to extract data from pdf file corresponding to comp

    :param company_name: name of company
    :param pdf_file: pdf file to extract
    :return: CompanyData object containing extracted data
    """

    # realistically, this might be replaced by a table containing records of uploaded company files.
    file_path = COMPANY_NAME_FILE_PATH_MAPPING[company_name]

    # a real service might take a token in the request header, but using hard-coded key here for mocked service.
    pdfs = PdfService(key="TEST_KEY")
    return parse_company_data(pdfs.extract(file_path=file_path))


