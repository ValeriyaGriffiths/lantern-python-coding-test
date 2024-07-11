from src.pdf_service import PdfService
from src.data_layer import parse_company_data
from src.models import CompanyData
from src.config import settings


def extract_and_parse_pdf_data(company_name: str, pdf_file) -> CompanyData:
    """
    Calls PdfService to extract data from pdf file corresponding to comp

    :param company_name: name of company
    :param pdf_file: pdf file to extract
    :return: CompanyData object containing extracted data
    """

    # this is a mocked service
    pdfs = PdfService(key=settings.api_key)

    # realistically, we might want a db table containing records of uploaded company files with
    # e.g. company_name, file_path, etc.
    # ignoring pdf_file and parsing company_name directly into file path for simplicity.
    extracted_company_data = (pdfs.extract(file_path=f"assets/{company_name.lower()}.pdf"))
    return CompanyData(**extracted_company_data)
