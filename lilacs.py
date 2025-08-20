import contextlib
import pandas as pd
import ast
from ETL import extract, load
import datetime as dt


@contextlib.contextmanager
def timer():
  """Time the execution of a context block.

  Yields:
    None
  """
  start = dt.datetime.now()
  # Send control back to the context block
  yield
  end = dt.datetime.now()
  total = end - start
  print('Elapsed: ',total)

# Cargar archivo
filepath = 'C:/LILACS_17_06_2025.csv'


with timer():
    df = extract(filepath)
    
print(df.head())
print(df.shape)


lang = ('es','pt','fr','en')

dferr = df[~df['Language'].isin(lang)]

print(dferr[['ID','Language']].head())

df=df[df['Language'].isin(lang)]

print('Total records on original .csv file: {}'.format(dferr.shape[0]+df.shape[0]))
print('Error on load records:',dferr.shape[0])
print('Succesfully loaded records:',df.shape[0])
print('Rate of success: {value:.2f}%'.format(value=df.shape[0]/(dferr.shape[0]+df.shape[0])*100))


load(df)

