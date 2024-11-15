import unittest
from unittest.mock import patch, MagicMock
import requests
from io import StringIO
import csv
from main import get_divar_urls, fetch_product_details, save_to_csv  # Assuming your main code is in a file named app.py

class TestDivarApp(unittest.TestCase):

    @patch('requests.get')
    def test_get_divar_urls(self, mock_get):
        # Mocking the response for the search API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "urls": ["https://divar.ir/v/sample-product-1", "https://divar.ir/v/sample-product-2"],
            "lastPostDate": "2024-11-01T08:00:00.123456Z"
        }
        mock_get.return_value = mock_response

        # Call the function with test parameters
        urls = get_divar_urls(query="207", city_id="38", page_limit=3)

        # Assertions
        self.assertEqual(len(urls), 2)
        self.assertIn("https://divar.ir/v/sample-product-1", urls)
        self.assertIn("https://divar.ir/v/sample-product-2", urls)

    @patch('requests.get')
    def test_fetch_product_details(self, mock_get):
        # Mocking the response for the product details API
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"title": "کارکرد", "value": "1"},
            {"title": "مدل (سال تولید)", "value": "1403"}
        ]
        mock_get.return_value = mock_response

        # Call the function with a sample tag
        product_details = fetch_product_details(tag="gZTHQDZy")

        # Assertions
        self.assertIsNotNone(product_details)
        self.assertEqual(len(product_details), 2)
        self.assertEqual(product_details[0]["title"], "کارکرد")
        self.assertEqual(product_details[0]["value"], "1")
        self.assertEqual(product_details[1]["title"], "مدل (سال تولید)")
        self.assertEqual(product_details[1]["value"], "1403")

    def test_save_to_csv(self):
        # Sample data to save to CSV
        data = [
            [
                {"title": "کارکرد", "value": "1"},
                {"title": "مدل (سال تولید)", "value": "1403"}
            ],
            [
                {"title": "کارکرد", "value": "2"},
                {"title": "مدل (سال تولید)", "value": "1404"}
            ]
        ]

        # Use StringIO to capture the CSV output
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            save_to_csv(data, filename="test.csv")

            # Check if the file write is called
            mock_file.assert_called_once_with("test.csv", mode="w", newline="", encoding="utf-8")

            # Check that the correct content was written to the file
            handle = mock_file()
            written_data = handle.write.call_args_list
            written_data = [call[0][0] for call in written_data]

            # Check header and data
            self.assertIn("مدل (سال تولید),کارکرد\r\n", written_data[0])
            self.assertIn("1403,1\r\n", written_data[1])
            self.assertIn("1404,2\r\n", written_data[2])

if __name__ == "__main__":
    unittest.main()
