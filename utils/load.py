from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def connection_db (db_url, df):
  ''' connect to databse and load to sheets via api'''
  try :
    engine = create_engine(db_url)

    with engine.connect() as con:
      df['timestamp'] = df['timestamp'].astype(str)
      df.to_sql('scraping', con = con, if_exists = 'append', index = False)
      print('Data loaded successfully')
  except Exception as e:
    print(f"An error occurred: {e}")

def sheet_load(df, service, scope, ID, range_name):
  credential = Credentials.from_service_account_file(service, scopes=scope)
  try:
    service = build('sheets', 'v4', credentials = credential)
    sheet = service.spreadsheets()
    df['timestamp'] = df['timestamp'].astype(str)
    values = df.values.tolist()
    body ={
        'values':values
    }
    result = sheet.values().update(
        spreadsheetId = ID,
        range = range_name,
        valueInputOption = 'RAW',
        body = body

    ).execute()

    print('added to spreadsheets')

  except Exception as e:
    print(f"An error occurred: {e}")