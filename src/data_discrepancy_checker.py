from dataclasses import fields
from src.models import CompanyData, MismatchedFields, DataDiscrepancyCheckerResponse


def validate_company_data(extracted_data: CompanyData, stored_data: CompanyData) -> DataDiscrepancyCheckerResponse:
    """
    Returns a response object containing extracted_data, stored_data and any mismatched fields.
    """
    mismatched_fields = get_mismatched_fields(extracted_data=extracted_data, stored_data=stored_data)

    return DataDiscrepancyCheckerResponse(uploaded_data=extracted_data,
                                          stored_data=stored_data,
                                          mismatched_fields=mismatched_fields)


def get_mismatched_fields(extracted_data: CompanyData, stored_data: CompanyData) -> list[MismatchedFields]:
    """
    Compares extracted_data and stored_data and returns a list of mismatched fields if any are found.

    :param extracted_data: CompanyData object containing extracted pdf data
    :param stored_data: CompanyData object to compare extracted data against
    :return: list containing mismatched fields (if any)
    """
    extracted_dict = extracted_data.model_dump()
    stored_dict = stored_data.model_dump()

    mismatched_fields = []
    for key in extracted_dict.keys():
        stored = stored_dict.get(key)
        uploaded = extracted_dict.get(key)
        if stored != uploaded:
            mismatched_fields.append(MismatchedFields(field_name=key, uploaded_value=uploaded, stored_value=stored))

    return mismatched_fields

