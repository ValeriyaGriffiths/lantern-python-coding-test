# Write your tests here
import unittest
from decimal import Decimal
from unittest.mock import patch
from src.data_layer import load_company_data, parse_company_data, COMPANY_DATA_KEY_MAPPING
from src.models import CompanyData, DataDiscrepancyCheckerResponse, MismatchedFields


class TestDataLayer(unittest.TestCase):
    partial_company_data = dict(
        company_name='HealthInc',
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
        company_data_obj = CompanyData(
            company_name='HealthInc',
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
        validator_resp = DataDiscrepancyCheckerResponse(stored_data=company_data_obj,
                                                        uploaded_data=company_data_obj,
                                                        mismatched_fields=mock_mismatched_data)
        expected_result = ('{"uploaded_data": {"company_name": "HealthInc", "industry": "Healthcare", '
                           '"market_capitalization": 3000.0, "revenue": 1000.0, "ebitda": 250, "net_income": 80, '
                           '"debt": 150, "equity": 666, "enterprise_value": 3150, "pe_ratio": 15, '
                           '"revenue_growth_rate": 12, "ebitda_margin": 40, "net_income_margin": 8, "roe": 13.33, '
                           '"roa": 10, "current_ratio": 1, "debt_to_equity_ratio": 0.25, "location": "New York, NY", '
                           '"ceo": "Jane Smith", "number_of_employees": 3000}, "stored_data": {"company_name": '
                           '"HealthInc", "industry": "Healthcare", "market_capitalization": 3000.0, "revenue": '
                           '1000.0, "ebitda": 250, "net_income": 80, "debt": 150, "equity": 666, "enterprise_value": '
                           '3150, "pe_ratio": 15, "revenue_growth_rate": 12, "ebitda_margin": 40, '
                           '"net_income_margin": 8, "roe": 13.33, "roa": 10, "current_ratio": 1, '
                           '"debt_to_equity_ratio": 0.25, "location": "New York, NY", "ceo": "Jane Smith", '
                           '"number_of_employees": 3000}, "mismatched_fields": [{"field_name": "fake name", '
                           '"uploaded_value": "fake value", "stored_value": "fake value"}]}')

        result = validator_resp.to_json()

        self.assertEqual(result, expected_result)


class TestAPI(unittest.TestCase):
    def test_foo(self):
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
