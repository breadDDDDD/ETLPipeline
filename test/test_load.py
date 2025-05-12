import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import connection_db 

class TestDatabaseConnection(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'timestamp': ['2025-05-12 10:00:00', '2025-05-12 10:05:00'],
            'data': [10, 20]
        })
        self.db_url = 'postgresql://user:password@localhost:5432/mydatabase'

    @patch('utils.load.create_engine')  
    @patch('pandas.DataFrame.to_sql')  
    def test_connection_and_data_sending(self, mock_to_sql, mock_create_engine):

        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_connection = MagicMock()
        mock_engine.connect.return_value = mock_connection

        connection_db(self.db_url, self.df)
        mock_create_engine.assert_called_once_with(self.db_url)

        mock_to_sql.assert_called_once()

if __name__ == '__main__':
    unittest.main()