import pytest
import requests
from unittest.mock import patch
from divar_scraper import get_divar_urls, fetch_product_details, extract_tag_from_url, save_to_csv

# Mock the requests.get call to avoid making actual API requests during tests

@pytest.fixture
def mock_get():
    with patch("requests.get") as mock_get:
        yield mock_get

def test_get_divar_urls(mock_get):
    # Test successful response from Divar API
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "urls": [
            "https://divar.ir/v/پژو-207i-دنده‌ای-TU3،-مدل-۱۴۰۲/wZiY0NfM",
            "https://divar.ir/v/پژو-206-مدل-۱۴۰۱/abcd1234"
        ],
        "lastPostDate": "2024-11-01T08:00:00.123456Z"
    }

    urls = get_divar_urls(query="207", city_id="38", page_limit=3)
    assert len(urls) == 2
    assert "https://divar.ir/v/پژو-207i-دنده‌ای-TU3،-مدل-۱۴۰۲/wZiY0NfM" in urls
    assert "https://divar.ir/v/پژو-206-مدل-۱۴۰۱/abcd1234" in urls

def test_fetch_product_details(mock_get):
    # Test successful product details fetch
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"title": "کارکرد", "value": "1"},
        {"title": "مدل (سال تولید)", "value": "1403"},
        {"title": "رنگ", "value": "مشکی"},
    ]

    product_details = fetch_product_details(tag="gZTHQDZy")
    assert product_details is not None
    assert len(product_details) == 3
    assert product_details[0]["title"] == "کارکرد"
    assert product_details[1]["title"] == "مدل (سال تولید)"
    assert product_details[2]["title"] == "رنگ"

def test_extract_tag_from_url():
    # Test extracting the tag from the Divar product URL
    url = "https://divar.ir/v/207-%DA%AF%DB%8C%D8%B1%D8%A8%DA%A9%D8%B3-%D8%A7%D8%AA%D9%88%D9%85%D8%A7%D8%AA%DB%8C%DA%A9/gZTHQDZy"
    tag = extract_tag_from_url(url)
    assert tag == "gZTHQDZy"

def test_save_to_csv():
    # Test saving product details to CSV
    data = [
        [{"title": "کارکرد", "value": "1"}, {"title": "مدل (سال تولید)", "value": "1403"}, {"title": "رنگ", "value": "مشکی"}],
        [{"title": "کارکرد", "value": "2"}, {"title": "مدل (سال تولید)", "value": "1402"}, {"title": "رنگ", "value": "سفید"}]
    ]
    
    with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
        save_to_csv(data, filename="test_product_details.csv")
        mock_file.assert_called_once_with("test_product_details.csv", mode="w", newline="", encoding="utf-8")
