import unittest
from unittest.mock import patch
import pandas as pd
from utils.transform import transform

class TestTransform(unittest.TestCase):

    def setUp(self):
        self.data = [
            {'title': 'Product test 1', 'price': '$100', 'ratings': '4.5', 'colors': '1', 'timestamp': '2025-05-12 10:00:00'},
            {'title': 'Product testt2', 'price': '$200', 'ratings': '4.0', 'colors': '2', 'timestamp': '2025-05-12 11:05:00'}
        ]
        self.rate = 16000

    @patch.object(transform, 'data_df')
    @patch.object(transform, 'clean_df')
    @patch.object(transform, 'currency_exchange')
    @patch.object(transform, 'dtype_change')
    
    def test_full_transform(self, mock_dtype_change, mock_currency_exchange, mock_clean_df, mock_data_df):

        transformer = transform()
        mock_df = pd.DataFrame(self.data)
        mock_data_df.return_value = mock_df
        mock_clean_df.return_value = mock_df
        mock_currency_exchange.return_value = mock_df
        mock_dtype_change.return_value = mock_df

        result = transformer.full_transform(self.data, self.rate)

        self.assertIsInstance(result, pd.DataFrame)
        mock_data_df.assert_called_once_with(self.data)
        mock_clean_df.assert_called_once_with(mock_df)
        mock_currency_exchange.assert_called_once_with(mock_df, self.rate)
        mock_dtype_change.assert_called_once_with(mock_df)

if __name__ == '__main__':
    unittest.main()