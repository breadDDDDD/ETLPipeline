import pandas as pd
import numpy as np

class transform :

  ''' change from USD to rupiah, change datatypes, erase nulls/unknown values '''

  def data_df (self,data):
    df = pd.DataFrame(data)
    return df

  def clean_df(self,df):
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df = df[df['price'] != 'Not Available']
    df = df[df['title'] != 'Unknown Product']
    df = df[df['ratings'] != 'Rating']
    df = df[df['ratings'] != 'Not Rated']
    return df

  def currency_exchange(self, df, rate):
    df['price'] = df['price'].str.replace(r'[\$,]', '', regex=True).astype(float)
    df['price'] = df['price'] * rate
    return df

  def dtype_change(self, df):
    df['ratings'] = df['ratings'].astype(float)
    df['colors'] = df['colors'].astype(int)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

  def full_transform(self, data, rate ):
    try:
      df = self.data_df(data)
      df = self.clean_df(df)
      df = self.currency_exchange(df, rate)
      df = self.dtype_change(df)
      return df

    except Exception as e:
      print(f'error : {e}')