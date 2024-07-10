# from dataclasses import fields
# from models import CompanyData, DataDifference


# def validate(uploaded_data: CompanyData, stored_data: CompanyData) -> list[DataDifference]:
#     mismatched_fields: list = []

#     for field in fields(CompanyData):
#         uploaded_field = getattr(uploaded_data, field.name)
#         stored_field = getattr(stored_data, field.name)
#         if uploaded_data != stored_data:
#             mismatched_fields.append(DataDifference(field_name=field.name, uploaded_value=uploaded_field, stored_value=stored_field)) 

#     return mismatched_fields


# def get_mismatched_attributes(self, other):
#     return [f.name for f in dataclasses.fields(self) if self.__getattribute__(f.name) != other.__getattribute__(f.name)]
