# LILACS

Files: 
- lilacs.py uses the read_csv pandas method for extraction of data. -
- cargar_df_lilacs.py is the main file of this project in which code I explore different ways to do the ETL. At the end of the file we explore the data we some general plotting.
- ETL.py includes the alternative_extraction method among many others (here it is the load method that loads the extracted data to the postgresql database on local host) used in cargar_lilacs_df.py
- plottinglilacs.py does the general and specific plotting (this last one requiring user inputs)
- pre_process_csv.py does what the name says, the output is the file we want to use in the alternative_extraction method.
- keyw.py goes further on the data analysis of communication and health theses.
