from src.pdf_service import PdfService
from src.data_layer import parse_company_data
from src.models import CompanyData


def extract_and_parse_pdf_data(company_name: str, pdf_file) -> CompanyData:
    """
    Calls PdfService to extract data from pdf file corresponding to comp

    :param company_name: name of company
    :param pdf_file: pdf file to extract
    :return: CompanyData object containing extracted data
    """

    # passing this in from data checker a real service might take a token in the request header, but using hard-coded key here for mocked service.
    pdfs = PdfService(key="TEST_KEY")

    # realistically, we might want a db table containing records of uploaded company files with
    # e.g. company_name, file_path, etc.
    # passing parsed company_name to mocked service here for simplicity.
    return parse_company_data(pdfs.extract(file_path=f"assets/{company_name.lower()}.pdf"))


