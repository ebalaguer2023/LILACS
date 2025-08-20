import pandas as pd
import datetime as dt
import contextlib
from plotlilacs import plotting
from ETL import load, alternative_extraction, convert
import os
import numpy as np

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
  
  


# the input file
file = 'LILACS_17_06_2025_step3.csv'

#file='fortune.csv'

sep = ','
#########################################################################
with timer():
    df = alternative_extraction(file,sep)

print(df.head())
print(df.shape)

##The original file contains failures on the closures of the strings that shift values
##when this happens the column 'Language' contains values that doesn´t belong to 
##the admited values, we will use a dictionary to control that column and exclude them off the df
lang = {"es" : "español", "pt": "português", "fr": "française", "en": "english"}
#lang = ('es','pt','fr','en') #before the dict I tried a list

dferr = df[~df['Language'].isin(lang)]
dferr.iloc[:,0:7].to_csv('revisar.csv', index=False, encoding='utf-8')
df=df[df['Language'].isin(lang)]



print('Total records on original .csv file: {}'.format(dferr.shape[0]+df.shape[0]))
print('Fails on extracted records:',dferr.shape[0])
print('Succesfully extracted records:',df.shape[0])
print('Rate of success: {value:.2f}%'.format(value=df.shape[0]/(dferr.shape[0]+df.shape[0])*100))

#########################################################################
# print(df.info())



# plotting general df

plotting(df, lang)

#########################################################################
##load df to database on local host, replacing table named 'lilacs'

load(df)

# ##These are empty columns, so I just dropped them after loading
df.drop(columns=['Volume number','Issue number','ISSN','Accession number','PMCID'])   

#########################################################################
#plotting special searches
print('Input for special searches (first input words, sequences of characters or regular expression to search in keywords and descriptors, then input title specifications for plots, eg: "about flu"')
inputsearch=input('Input for searches (words, sequences of characters or regular expression):')
title=input('Input for searches title specifications:')
df = df[df['Descriptor(s)'].str.contains(inputsearch, case=False) | df['Keyword(s)'].str.contains(inputsearch, case=False)]
selection = 'tesis '+title+'.csv'
df.to_csv(selection, index=False)
plotting(df, lang, title)


convert(df)

