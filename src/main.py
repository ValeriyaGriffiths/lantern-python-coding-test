from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from data_layer import load_company_data, parse_company_data
# from data_validator import validate
from models import CompanyData, MismatchedFields, DataDiscrepancyCheckerResponse
from pdf_service import PdfService


pdfs = PdfService(key="TEST_KEY")

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/company/validate-pdf")
def validate_company_pdf(company_name: str, data_file: UploadFile = File(...)):
    """
    Take company name and a pdf with company data and validates the data against stored data.
    Returns extracted pdf data, stored data, and list of mismatched fields.

    Assumed that we take company_name as an input (not super clear from README).
    """

    stored_data = load_company_data(company_name)

    if not stored_data: 
        # TODO
        return JSONResponse(status_code=500)

    extracted_data: CompanyData = parse_company_data(pdfs.extract(file_path="assets/retailco.pdf"))

    mismatched_fields: list[MismatchedFields] = []
    # validate(uploaded_data=extracted_data, stored_data=stored_data)

    validator_response = DataDiscrepancyCheckerResponse(uploaded_data=extracted_data, stored_data=stored_data, mismatched_fields=mismatched_fields)
    

    # assumed company name is provided by user, assume exact match
    # env var or pass in as a header
    # hash file content for idempotency key <- file path; reject if identical name 
    # read data from csv and deserialise
    # get data from pdf service -> by file path
    # output {company_name: {pdf: ..., stored:..., match: true/false}}
    #  uploaded_data: {.... }, stored_data: {.. } mismatched_fields: {company_name, stock_price,}
    # could reduce payload size later

    return JSONResponse(content=validator_response.to_json(), status_code=200)

