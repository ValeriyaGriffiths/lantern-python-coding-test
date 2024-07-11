from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from src.data_layer import load_company_data
from src.data_discrepancy_checker import validate_company_data
from src.pdf_service_api import extract_and_parse_pdf_data

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/company/validate-pdf-data")
async def validate_pdf_company_data(company_name: str, data_file: UploadFile = File(...)):
    """
    Take company name and a pdf with company data and validate the data against stored data.
    Returns extracted pdf data, stored data, and list of mismatched fields.

    :param company_name: company name
    :param data_file: pdf containing company data
    :return: json response with format matching DataDiscrepancyCheckerResponse
    """
    company_name= company_name.strip()

    stored_data = load_company_data(company_name)
    if not stored_data:
        return JSONResponse(content={"error": "No data found for this company name."}, status_code=500)

    try:
        extracted_data = extract_and_parse_pdf_data(company_name=company_name, pdf_file=data_file)
    except FileNotFoundError as ex:
        return JSONResponse(content={"error": ex.args[0]}, status_code=400)

    validated_response = validate_company_data(extracted_data=extracted_data, stored_data=stored_data)
    return JSONResponse(content=validated_response.to_json(), status_code=200)
