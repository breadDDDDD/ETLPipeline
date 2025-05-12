import unittest
from unittest.mock import patch
from datetime import datetime
import requests
from utils.extract import fetch, scrape_web


class TestWebScraper(unittest.TestCase):
    def setUp(self):
        self.sample_html = '''
        
        <div class='collection-card'>
            <div class='product-details'>
                <h3 class='product-title'>Test Product</h3>
                <p style='font-size: 14px; color: #777;'>Rating: 4.5 / 5</p>
                <p style='font-size: 14px; color: #777;'>Red</p>
                <p style='font-size: 14px; color: #777;'>Size: L</p>
                <p style='font-size: 14px; color: #777;'>Gender: Unisex</p>
                <div class='price-container'>
                    <span class='price'>$300</span>
                </div>
            </div>
        </div>
        
        '''

    @patch('requests.Session.get')
    def test_fetch_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.sample_html.encode()  # Encode to bytes
        result = fetch("https://example.com")
        
        self.assertIsNotNone(result)
        self.assertIn("Test Product", result.decode())  # Decode to string

    @patch('requests.Session.get')
    def test_fetch_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Not Found")
        result = fetch("https://invalid-url.com")
        
        self.assertIsNone(result)

    @patch('utils.extract.fetch')
    def test_scrape_web(self, mock_fetch):
        mock_fetch.return_value = self.sample_html
        result = scrape_web("https://example.com")
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
        item = result[0]
        
        self.assertEqual(item['title'], 'Test Product')
        self.assertEqual(item['price'], '$300')
        self.assertEqual(item['ratings'], '4.5') 
        self.assertEqual(item['colors'], 'Red')
        self.assertEqual(item['size'], 'L')
        self.assertEqual(item['gender'], 'Unisex')
        self.assertIn('timestamp', item)

    @patch('utils.extract.fetch')
    def test_scrape_web_empty_content(self, mock_fetch):
        mock_fetch.return_value = None
        result = scrape_web("https://example.com")
        
        self.assertEqual(result, [])

    @patch('utils.extract.fetch')
    def test_scrape_web_no_next_page(self, mock_fetch):
        mock_fetch.return_value = self.sample_html
        result = scrape_web("https://example.com")
        
        self.assertEqual(len(result), 1)
        self.assertIn('timestamp', result[0])

if __name__ == '__main__':
    unittest.main()
