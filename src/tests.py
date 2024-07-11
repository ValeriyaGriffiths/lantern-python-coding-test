import io
import unittest
from unittest.mock import patch
from decimal import Decimal
from src.data_discrepancy_checker import get_mismatched_fields, validate_company_data
from src.data_layer import load_company_data
from src.models import CompanyData, DataDiscrepancyCheckerResponse, MismatchedFields
from fastapi.testclient import TestClient
from main import app
from src.pdf_service_api import extract_and_parse_pdf_data

test_company_data = {
    'Company Name': 'HealthInc',
    'Industry': 'Healthcare',
    'Market Capitalization': 3000,
    'Revenue (in millions)': 1000,
    'EBITDA (in millions)': 250,
    'Net Income (in millions)': 80,
    'Debt (in millions)': 150,
    'Equity (in millions)': 666,
    'Enterprise Value (in millions)': 3150,
    'P/E Ratio': 15,
    'Revenue Growth Rate (%)': 12,
    'EBITDA Margin (%)': 40,
    'Net Income Margin (%)': 8,
    'ROE (Return on Equity) (%)': 13.33,
    'ROA (Return on Assets) (%)': 10,
    'Debt to Equity Ratio': 0.25,
    'Location': 'New York, NY',
    'CEO': 'Jane Smith',
    'Number of Employees': 3000,
}


class TestDataLayer(unittest.TestCase):

    def test_load_company_data(self):
        """
        Expect load_company_data to return company data from database.csv matching company_name.
        """
        company_name = "TechCorp"
        exp_res = CompanyData(
            **{'company_name': 'TechCorp', 'industry': 'Technology', 'market_capitalization': Decimal('5000'),
               'revenue': Decimal('1500'), 'ebitda': Decimal('300'), 'net_income': Decimal('100'),
               'debt': Decimal('200'),
               'equity': Decimal('800'), 'enterprise_value': Decimal('5400'), 'pe_ratio': Decimal('25'),
               'revenue_growth_rate': Decimal('10'), 'ebitda_margin': Decimal('20'),
               'net_income_margin': Decimal('6.67'),
               'roe': Decimal('12.5'), 'roa': Decimal('7.5'), 'current_ratio': Decimal('2.5'),
               'debt_to_equity_ratio': Decimal('0.25'), 'location': 'San Francisco', 'ceo': None,
               'number_of_employees': None})

        result = load_company_data(company_name)

        self.assertEqual(result, exp_res)

    def test_load_company_data_name_not_found(self):
        """
        Expect load_company_data to return None when company_name not found in stored data.
        """
        company_name = "Fake Company"

        result = load_company_data(company_name)

        self.assertIsNone(result)


class TestDataDiscrepancyChecker(unittest.TestCase):
    def setUp(self):
        self.company_data1 = CompanyData(**test_company_data)
        self.company_data2 = CompanyData(**test_company_data)
        self.company_data2.company_name = 'Fake Company'
        self.company_data2.revenue = 111
        self.company_data2.number_of_employees = None
        mismatched_field_names = ['company_name', 'revenue', 'number_of_employees']
        self.mismatched_fields = [
            MismatchedFields(field_name=f, stored_value=getattr(self.company_data1, f),
                             uploaded_value=getattr(self.company_data2, f))
            for f in mismatched_field_names
        ]

    def test_get_mismatched_fields_empty_list(self):
        """
        Expect get_mismatched_fields to return empty list for identical data.
        """

        result = get_mismatched_fields(stored_data=self.company_data1, extracted_data=self.company_data1)

        self.assertEqual(result, [])

    def test_get_mismatched_fields(self):
        """
        Expect get_mismatched_fields to return a list of mismatched fields.
        """
        result = get_mismatched_fields(stored_data=self.company_data1, extracted_data=self.company_data2)

        self.assertEqual(result, self.mismatched_fields)

    @patch("src.data_discrepancy_checker.get_mismatched_fields")
    def test_validate_company_data(self, mock_get_mismatched_fields):
        """
        Expect get_mismatched_fields to be called and DataDiscrepancyCheckerResponse to be returned
        """
        expected_result = DataDiscrepancyCheckerResponse(uploaded_data=self.company_data1,
                                                         stored_data=self.company_data2,
                                                         mismatched_fields=self.mismatched_fields)
        mock_get_mismatched_fields.return_value = self.mismatched_fields

        result = validate_company_data(extracted_data=self.company_data1,
                                       stored_data=self.company_data2)

        mock_get_mismatched_fields.assert_called_once_with(extracted_data=self.company_data1,
                                                           stored_data=self.company_data2)
        self.assertEqual(result, expected_result)


@patch('main.validate_company_data')
@patch('main.extract_and_parse_pdf_data')
@patch('main.load_company_data')
class TestAPI(unittest.TestCase):
    client = TestClient(app)

    def setUp(self):
        self.file_like = io.BytesIO(b'fake pdf file.')

    def test_validate_pdf_company_data(self, mock_load_company_data, mock_extract_and_parse_pdf_data,
                                       mock_validate_company_data):
        """
        Expect validated response from validate_pdf_company_data endpoint.
        """

        # Mocking the response of the POST request
        mock_company_data = CompanyData(**test_company_data)
        mock_mismatched_data = [
            MismatchedFields(field_name='fake name', stored_value='fake value', uploaded_value='fake value')]
        validated_resp = DataDiscrepancyCheckerResponse(stored_data=mock_company_data,
                                                        uploaded_data=mock_company_data,
                                                        mismatched_fields=mock_mismatched_data)
        mock_load_company_data.return_value = 'fake data'
        mock_extract_and_parse_pdf_data.return_value = 'fake data'
        mock_validate_company_data.return_value = validated_resp

        resp = self.client.post(
            '/company/validate-pdf-data',
            params={'company_name': 'fake company name'},
            files={'data_file': ('test_file.txt', self.file_like, 'application/pdf')}
        )

        exp_res = {'uploaded_data': {'company_name': 'HealthInc', 'industry': 'Healthcare',
                                     'market_capitalization': '3000', 'revenue': '1000', 'ebitda': '250',
                                     'net_income': '80', 'debt': '150', 'equity': '666', 'enterprise_value': '3150',
                                     'pe_ratio': '15', 'revenue_growth_rate': '12', 'ebitda_margin': '40',
                                     'net_income_margin': '8', 'roe': '13.33', 'roa': '10', 'current_ratio': None,
                                     'debt_to_equity_ratio': '0.25', 'location': 'New York, NY', 'ceo': 'Jane Smith',
                                     'number_of_employees': 3000},
                   'stored_data': {'company_name': 'HealthInc', 'industry': 'Healthcare',
                                   'market_capitalization': '3000', 'revenue': '1000', 'ebitda': '250',
                                   'net_income': '80', 'debt': '150', 'equity': '666', 'enterprise_value': '3150',
                                   'pe_ratio': '15', 'revenue_growth_rate': '12', 'ebitda_margin': '40',
                                   'net_income_margin': '8', 'roe': '13.33', 'roa': '10', 'current_ratio': None,
                                   'debt_to_equity_ratio': '0.25', 'location': 'New York, NY', 'ceo': 'Jane Smith',
                                   'number_of_employees': 3000},
                   'mismatched_fields': [
                       {'field_name': 'fake name', 'uploaded_value': 'fake value', 'stored_value': 'fake value'}]}
        self.assertEqual(resp.json(), exp_res)
        self.assertEqual(resp.status_code, 200)

    def test_validate_pdf_company_data_return_data_error(self, mock_load_company_data, mock_extract_and_parse_pdf_data,
                                                         mock_validate_company_data):
        """
        Expect error response if no stored data found.
        """

        mock_load_company_data.return_value = None

        resp = self.client.post(
            '/company/validate-pdf-data',
            params={'company_name': 'fake company name'},
            files={'data_file': ('test_file.txt', self.file_like, 'application/pdf')}
        )

        self.assertEqual(resp.json(), {"error": "No data found for this company name."})
        self.assertEqual(resp.status_code, 400)

    def test_validate_pdf_company_data_return_file_error(self, mock_load_company_data, mock_extract_and_parse_pdf_data,
                                                         mock_validate_company_data):
        """
        Expect error response if cannot extract file data.
        """

        mock_load_company_data.return_value = 'fake data'
        mock_extract_and_parse_pdf_data.side_effect = FileNotFoundError('fake ex')
        mock_validate_company_data.return_value.to_json.return_value = {'fake': 'response'}

        resp = self.client.post(
            '/company/validate-pdf-data',
            params={'company_name': 'fake company name'},
            files={'data_file': ('test_file.txt', self.file_like, 'application/pdf')}
        )

        self.assertEqual(resp.json(), {"error": "fake ex"})
        self.assertEqual(resp.status_code, 400)


class TestPdfServiceCaller(unittest.TestCase):
    @patch('pdf_service_api.PdfService.extract')
    def test_extract_and_parse_pdf_data(self, mock_extract):
        mock_extract.return_value = test_company_data

        extract_and_parse_pdf_data(company_name='FakeCompany', pdf_file='Fake File')

        mock_extract.assert_called_once_with(file_path="assets/fakecompany.pdf")


if __name__ == '__main__':
    unittest.main()
