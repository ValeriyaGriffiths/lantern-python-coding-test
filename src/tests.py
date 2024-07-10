# Write your tests here
import unittest
from decimal import Decimal
from unittest.mock import patch
from src.data_layer import load_company_data, parse_company_data
from src.models import CompanyData


class TestDataLayer(unittest.TestCase):
    @patch('src.data_layer.parse_company_data')
    def test_load_company_data(self, mock_parse_company_data):
        """
        return company by name. mock parse_company_data called once.
        realistically we would have a db anyway.
        """
        mock_parse_company_data.return_value = 'mocked_result'
        company_name = "TechCorp"

        result = load_company_data(company_name)

        mock_parse_company_data.assert_called_once()
        self.assertEqual(result, 'mocked_result')

    @patch('src.data_layer.parse_company_data')
    def test_load_company_data_name_not_found(self, mock_parse_company_data):
        company_name = "Fake Company"

        result = load_company_data(company_name)

        mock_parse_company_data.assert_not_called()
        self.assertIsNone(result)

    def test_parse_company_data(self):
        """
        test all fields match
        """
        company_data_dict = {
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
            'Current Ratio': 1,
            'Debt to Equity Ratio': 0.25,
            'Location': 'New York, NY',
            'CEO': 'Jane Smith',
            'Number of Employees': 3000
        }
        expected_result = CompanyData(
            company_name=company_data_dict['Company Name'],
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

        result = parse_company_data(company_data_dict)

        self.assertEqual(result, expected_result)

    def test_parse_company_data_bad_input(self):
        """
        bad dict, containing wierd shit.
        :return:
        """
        pass


class TestAPI(unittest.TestCase):
    def test_foo(self):
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
