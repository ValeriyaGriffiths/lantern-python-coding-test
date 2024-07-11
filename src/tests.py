import unittest
import requests
from unittest.mock import patch, Mock
from src.data_discrepancy_checker import get_mismatched_fields, validate_company_data
from src.data_layer import load_company_data, parse_company_data, COMPANY_DATA_KEY_MAPPING
from src.models import CompanyData, DataDiscrepancyCheckerResponse, MismatchedFields


class TestDataLayer(unittest.TestCase):
    partial_company_data = dict(
        company_name='Fake',
        industry='Healthcare',
        market_capitalization=3000.0,
        revenue=1000.00,
        ebitda=250,
        net_income=80,
        debt=150,
        equity=666,
        enterprise_value=3150,
        pe_ratio=15,
        revenue_growth_rate=12,
        ebitda_margin=40,
        net_income_margin=8,
        roe=13.33,
        roa=10,
        current_ratio=1,
        debt_to_equity_ratio=0.25,
        location='New York, NY',
    )
    company_data = partial_company_data | dict(
        ceo='Jane Smith',
        number_of_employees=3000,
    )

    def _parse_obj_to_dict(self, company_data: dict):
        return {COMPANY_DATA_KEY_MAPPING[k]: v for k, v in company_data.items()}

    @patch('src.data_layer.parse_company_data')
    def test_load_company_data(self, mock_parse_company_data):
        """
        Expect load_company_data to return company data from database.csv matching company_name.
        """
        mock_parse_company_data.return_value = 'mocked_result'
        company_name = "TechCorp"

        result = load_company_data(company_name)

        mock_parse_company_data.assert_called_once()
        self.assertEqual(result, 'mocked_result')

    @patch('src.data_layer.parse_company_data')
    def test_load_company_data_name_not_found(self, mock_parse_company_data):
        """
        Expect load_company_data to return None when company_name not found in stored data.
        """
        company_name = "Fake Company"

        result = load_company_data(company_name)

        mock_parse_company_data.assert_not_called()
        self.assertIsNone(result)

    def test_parse_company_data(self):
        """
        Expect parse_company_data to return a CompanyData object corresponding to provided dict.
        """
        company_data_dict = self._parse_obj_to_dict(self.company_data)
        expected_result = CompanyData(**self.company_data)

        result = parse_company_data(company_data_dict)

        self.assertEqual(result, expected_result)

    def test_parse_company_data_missing_fields(self):
        """
        Expect parsed object to handle missing field values by returning None for those fields.
        """
        company_data_dict = self._parse_obj_to_dict(self.partial_company_data)
        expected_result = CompanyData(ceo=None, number_of_employees=None, **self.partial_company_data)

        result = parse_company_data(company_data_dict)

        self.assertEqual(result, expected_result)


class TestModels(unittest.TestCase):

    def test_ValidatorResponse_to_json(self):
        """

        :return:
        """
        mock_company_data = CompanyData(
            company_name='Fake',
            industry='Healthcare',
            market_capitalization=3000.0,
            revenue=1000.00,
            ebitda=250,
            net_income=80,
            debt=150,
            equity=666,
            enterprise_value=3150,
            pe_ratio=15,
            revenue_growth_rate=12,
            ebitda_margin=40,
            net_income_margin=8,
            roe=13.33,
            roa=10,
            current_ratio=1,
            debt_to_equity_ratio=0.25,
            location='New York, NY',
            ceo='Jane Smith',
            number_of_employees=3000,
        )
        mock_mismatched_data = [
            MismatchedFields(field_name='fake name', stored_value='fake value', uploaded_value='fake value')]
        validated_resp = DataDiscrepancyCheckerResponse(stored_data=mock_company_data,
                                                        uploaded_data=mock_company_data,
                                                        mismatched_fields=mock_mismatched_data)
        expected_result = ('{"uploaded_data": {"company_name": "Fake", "industry": "Healthcare", '
                           '"market_capitalization": 3000.0, "revenue": 1000.0, "ebitda": 250, "net_income": 80, '
                           '"debt": 150, "equity": 666, "enterprise_value": 3150, "pe_ratio": 15, '
                           '"revenue_growth_rate": 12, "ebitda_margin": 40, "net_income_margin": 8, "roe": 13.33, '
                           '"roa": 10, "current_ratio": 1, "debt_to_equity_ratio": 0.25, "location": "New York, NY", '
                           '"ceo": "Jane Smith", "number_of_employees": 3000}, "stored_data": {"company_name": '
                           '"Fake", "industry": "Healthcare", "market_capitalization": 3000.0, "revenue": '
                           '1000.0, "ebitda": 250, "net_income": 80, "debt": 150, "equity": 666, "enterprise_value": '
                           '3150, "pe_ratio": 15, "revenue_growth_rate": 12, "ebitda_margin": 40, '
                           '"net_income_margin": 8, "roe": 13.33, "roa": 10, "current_ratio": 1, '
                           '"debt_to_equity_ratio": 0.25, "location": "New York, NY", "ceo": "Jane Smith", '
                           '"number_of_employees": 3000}, "mismatched_fields": [{"field_name": "fake name", '
                           '"uploaded_value": "fake value", "stored_value": "fake value"}]}')

        result = validated_resp.to_json()

        self.assertEqual(result, expected_result)


class TestDataDiscrepancyChecker(unittest.TestCase):
    def setUp(self):
        self.company_data1 = CompanyData(
            company_name='Fake',
            industry='Healthcare',
            market_capitalization=3000.0,
            revenue=1000.00,
            ebitda=250,
            net_income=80,
            debt=150,
            equity=666,
            enterprise_value=3150,
            pe_ratio=15,
            revenue_growth_rate=12,
            ebitda_margin=40,
            net_income_margin=8,
            roe=13.33,
            roa=10,
            current_ratio=1,
            debt_to_equity_ratio=0.25,
            location='New York, NY',
            ceo='Jane Smith',
            number_of_employees=3000,
        )
        self.company_data2 = CompanyData(
            company_name='Fake Company',
            industry='Healthcare',
            market_capitalization=3000.0,
            revenue=2000,
            ebitda=250,
            net_income=80,
            debt=150,
            equity=666,
            enterprise_value=3150,
            pe_ratio=15,
            revenue_growth_rate=12,
            ebitda_margin=40,
            net_income_margin=8,
            roe=13.33,
            roa=10,
            current_ratio=1,
            debt_to_equity_ratio=0.25,
            location='New York, NY',
            ceo='Jane Smith',
            number_of_employees=None,
        )
        mismatched_field_names = ['company_name', 'revenue', 'number_of_employees']
        self.mismatched_fields = [
            MismatchedFields(field_name=f, stored_value=getattr(self.company_data1, f),
                             uploaded_value=getattr(self.company_data2, f))
            for f in mismatched_field_names
        ]

    @patch("src.data_discrepancy_checker.get_mismatched_fields")
    def test_validate_company_data(self, mock_get_mismatched_fields):
        """
        Expect get_mismatched_fields to be called and DataDiscrepancyCheckerResponse to be returned
        """
        mock_get_mismatched_fields.return_value = self.mismatched_fields
        expected_result = DataDiscrepancyCheckerResponse(uploaded_data=self.company_data1,
                                                         stored_data=self.company_data2,
                                                         mismatched_fields=self.mismatched_fields)

        result = validate_company_data(extracted_data=self.company_data1,
                                       stored_data=self.company_data2)

        mock_get_mismatched_fields.assert_called_once_with(extracted_data=self.company_data1,
                                                           stored_data=self.company_data2)
        self.assertEqual(result, expected_result)

    def test_get_mismatched_fields(self):
        """
        Expect get_mismatched_fields to return a list of mismatched fields.
        """
        result = get_mismatched_fields(stored_data=self.company_data1, extracted_data=self.company_data2)

        self.assertEqual(result, self.mismatched_fields)

    def test_get_mismatched_fields_empty_list(self):
        """
        Expect get_mismatched_fields to return empty list for identical data.
        """

        result = get_mismatched_fields(stored_data=self.company_data1, extracted_data=self.company_data1)

        self.assertEqual(result, [])


class TestPdfServiceApi(unittest.TestCase):
    @patch('src.pdf_service_api.parse_company_data')
    def test_extract_and_parse_pdf_data(self, mock_parse_company_data):
        pass


class TestAPI(unittest.TestCase):
    @patch('src.main.validate_company_data')
    def test_validate_pdf_company_data(self, mock_validate_company_data):
        """
        Expect validated response from validate_pdf_company_data endpoint.
        # TODO header with key?
        # hit the endpoint as a user; pass name and file, return json w data
        """
        mock_validate_company_data = Mock()
        mock_validate_company_data.return_value.to_json.return_value = {'fake': 'response'}

        resp = requests.get('http://example.com/api/123')

        self.assertEqual(resp.message, {'fake': 'response'})
        self.assertEqual(resp.status_code, 200)

    def test_validate_pdf_company_data_return_data_error(self):
        """
        Expect error response if no stored data found.
        """
        resp = None
        self.assertEqual(resp.message, "No data found for this company name.")
        self.assertEqual(resp.status_code, 500)

    def test_validate_pdf_company_data_return_file_error(self):
        """
        Expect error response if cannot extract file data.
        """
        resp = None
        self.assertEqual(resp.message,"Cannot extract data. Invalid file provided.")
        self.assertEqual(resp.status_code, 400)


if __name__ == '__main__':
    unittest.main()
