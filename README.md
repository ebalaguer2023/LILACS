# LILACS

ETL Essays with the LILACS Database
In order to incorporate new materials into the Communication and Health research database, I revisited the LILACS/BIREME database (https://lilacs.bvsalud.org/es/) to download records linked to academic theses. The database can be accessed by downloading the .csv file offered in the search section ("export" option), from which you can also obtain the XML for specific searches.
 

The way the .csv file is built causes certain records to be lost when imported and can even cause the import to fail completely. This happened using the pandas read_csv method, but also when trying different ways of importing .csv files for SQL Server Management Studio and PostgreSQL.
As I remembered the possibility of obtaining the data in XML format for specific queries, I wrote to the site administrators to see if there was an API to download the entire database in XML, but they soon replied that such an option did not currently exist.
So, I had no choice but to revisit the .csv file and analyze what the obstacles might be. So this is what I’ve found:
I) The problem seems to be with the quotation marks that (do not) enclose strings: Some appear improperly closed, and that's when the delimiter—a comma that should be inside the string—would be left outside the string and misinterpreted. II) II) To further complicate matters—although I assume this was originally intended to simplify things somewhat—two, three, four, or even five consecutive quotation marks can appear to refer to titles, proper names, or textual quotes.
Because of all this, the read_csv method simply fails if we try to import all the columns (the same happens if we try to use the Microsoft SQL Server Management Studio data import wizard). We may have better luck in pandas if we specify which columns we want to import, but even in this case, if we analyze the values obtained, we will see that some rows have been poorly parsed. 
alternative_extraction: Custom code to import the .csv file
Following these attempts, I decided to develop my own import method. It reads the file line by line and character by character. It interprets a value as a string when a quote appears, and that string value is closed before the next quote, so that commas within those quotes do not act as delimiters (this solves problem 1). I also developed preprocessing code that replaces quotes followed by a special character (this mitigates problem 2).

Performance Analysis of the pandas read_csv and alternative_extraction methods
Given the execution time and the number of correctly retrieved records (remember that, as we have seen, pandas can parse some rows incorrectly), the pandas read_csv method remains the most viable option for data analysis. While for a job that involves exhaustive retrieval of records and continuous improvement in ETL processes, alternative_extraction allows to retrieve a greater number of records -leaving less work for manual loading- with a rate of 99.96% of recovered records (compared to 99.46% that the method provided by pandas managed to retrieve). While read_csv returns 167 failed records -compared to the mere 11 offered by the ad hoc developed code-, the execution time is much better, alternative_extraction takes almost 23 seconds compared to 1 second (or even less) that the execution of pandas.read_csv takes.
 
Data Analysis
 


 

The general data analysis shows the predominance of Brazil as the main country of publications, and congruently, Portuguese as the language in which the majority of theses were written (24,138), followed by Spanish (6,244)—published in different Spanish-speaking countries—, English (236), and French (7). For every theses in Spanish, there are four in Portuguese. 2015 was the year with the highest number of theses published.
Regarding the theses that we would include in the field of communication and health—a very limited universe, with fewer than 500 records—the same proportions are maintained. Delving into the specifics of this particular field of research, a preliminary analysis of keywords and descriptors gives us an indication of the main topics of interest, but suggests the need to unify both fields and systematize the categories. In addition we can discard the keyword and descriptor “communication” because it’s obvious that it is present in our search.

