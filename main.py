
from utils.extract import scrape_web
from utils.transform import transform
from utils.load import connection_db
from utils.load import sheet_load

def main():

  ''' Main function to run all '''
  try:
    url = 'https://fashion-studio.dicoding.dev/'
    db_url = 'postgresql://developer:1234@localhost:5432/scrapingdb'
    service ='genial-airway-399715-924a29f4d3e9.json'
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    ID ='1ngffKhq3dLPz-edYyinx3xDXQa0ftmgljsdbqxkx1iM'
    range_name ='Sheet1'
    rates = 16000

    transformer = transform()
    all_item = scrape_web(url)
    df = transformer.full_transform(all_item, rates)
    sheet_load(df,service,scope,ID,range_name )
    connection_db(db_url, df)
    df.to_csv('products.csv', index=False)

    print(df)
    print(df.dtypes)
    return df

  except Exception as e:
    print(f"An error occurred: {e}")

if __name__ == '__main__':
  main()