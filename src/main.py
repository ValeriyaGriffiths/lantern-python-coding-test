from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from src.config import settings
from src.data_layer import load_company_data
from src.data_discrepancy_checker import validate_company_data
from src.pdf_service_api import extract_and_parse_pdf_data
from src.models import DataDiscrepancyCheckerResponse

app = FastAPI(debug=settings.debug)


@app.post("/company/validate-pdf-data", response_model=DataDiscrepancyCheckerResponse, response_model_by_alias=False)
async def validate_pdf_company_data(company_name: str, data_file: UploadFile = File(...)):
    """
    Take company name and a pdf with company data and validate the data against stored data.
    Returns extracted pdf data, stored data, and list of mismatched fields.

    :param company_name: company name
    :param data_file: pdf containing company data
    :return: json response with format matching DataDiscrepancyCheckerResponse
    """
    # strip any spaces to ensure we find the company file and data
    company_name = company_name.strip()

    stored_data = load_company_data(company_name)
    if not stored_data:
        return JSONResponse(content={"error": "No data found for this company name."}, status_code=400)

    try:
        extracted_data = extract_and_parse_pdf_data(company_name=company_name, pdf_file=data_file)
    except FileNotFoundError as ex:
        return JSONResponse(content={"error": ex.args[0]}, status_code=400)

    validated_response = validate_company_data(extracted_data=extracted_data, stored_data=stored_data)

    return validated_response
