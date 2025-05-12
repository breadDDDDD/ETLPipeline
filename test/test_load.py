import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import connection_db, sheet_load  # Adjust according to your actual module path

class TestDatabaseAndSheetOperations(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame for testing
        self.df = pd.DataFrame({
            'timestamp': ['2025-05-12 10:00:00', '2025-05-12 10:05:00'],
            'data': [10, 20]
        })

        self.db_url = 'postgresql://user:password@localhost:5432/mydatabase'
        self.scope = ['https://www.googleapis.com/auth/spreadsheets']
        self.service_account_file = 'path_to_service_account_file.json'  # This will be mocked
        self.sheet_id = 'your_sheet_id'
        self.range_name = 'Sheet1!A1'

    @patch('sqlalchemy.create_engine')
    @patch('pandas.DataFrame.to_sql')
    def test_connection_db(self, mock_to_sql, mock_create_engine):
        # Mock the database engine and connection
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_connection = MagicMock()
        mock_engine.connect.return_value = mock_connection

        # Ensure the to_sql method is mocked properly
        mock_to_sql.return_value = None

        # Run the function
        connection_db(self.db_url, self.df)

        # Verify that the to_sql method was called with the correct parameters
        mock_to_sql.assert_called_once_with('scraping', con=mock_connection, if_exists='append', index=False)

    @patch('googleapiclient.discovery.build')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    @patch('pandas.DataFrame.to_sql')  # Not strictly necessary for this test, but good practice to patch when not needed.
    def test_sheet_load(self, mock_to_sql, mock_from_service_account_file, mock_build):
        # Mock the Credentials.from_service_account_file method
        mock_credentials = MagicMock()
        mock_from_service_account_file.return_value = mock_credentials
        
        # Mock the Sheets API
        mock_service = MagicMock()
        mock_sheets = MagicMock()
        mock_service.spreadsheets.return_value = mock_sheets
        mock_build.return_value = mock_service

        # Mock the values().update() method to simulate a successful API call
        mock_update = MagicMock()
        mock_sheets.values.return_value.update.return_value = mock_update

        # Run the function
        sheet_load(self.df, self.service_account_file, self.scope, self.sheet_id, self.range_name)

        # Verify that the Google Sheets API update method was called
        mock_sheets.values.return_value.update.assert_called_once_with(
            spreadsheetId=self.sheet_id,
            range=self.range_name,
            valueInputOption='RAW',
            body={'values': self.df.values.tolist()}
        )


if __name__ == '__main__':
    unittest.main()
