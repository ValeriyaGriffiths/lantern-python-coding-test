from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from data_layer import load_company_data
from data_discrepancy_checker import validate_company_data
from src import pdf_service_api

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/company/validate-pdf-data")
def validate_pdf_company_data(company_name: str, data_file: UploadFile = File(...)):
    """
    Take company name and a pdf with company data and validate the data against stored data.
    Returns extracted pdf data, stored data, and list of mismatched fields.

    Assume that we take company_name as an input (not super clear from README).

   :param company_name: company name
   :param data_file: pdf containing company data
   :return: json response with format matching DataDiscrepancyCheckerResponse
   """

    stored_data = load_company_data(company_name)
    if not stored_data:
        return JSONResponse(content={"error": "No stored data found for this company"}, status_code=500)

    try:
        extracted_data = pdf_service_api.extract_and_parse_pdf_data(company_name=company_name, pdf_file=data_file)
    except FileNotFoundError as ex:
        return JSONResponse(content={"error": ex.args[0]}, status_code=500)

    validated_response = validate_company_data(extracted_data=extracted_data, stored_data=stored_data)
    return JSONResponse(content=validated_response.to_json(), status_code=200)
