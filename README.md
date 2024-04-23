# database-migration-data-challenge

Local REST API created using _FastAPI_ Python library to migrate data from three CSV files to corresponding _SQLite_ tables. 

Files to be migrated:
1. hired_employees.csv
2. departments.csv
3. jobs.csv

Two endpoints are provided to handle data:
* **GET** /Data/{file_id}

  It retrieves data from the CSV file identified by _{file_id}_ and displays it in JSON format, row by row.

* **POST** /Upload/{file_id}

  It gets data from the CSV file identified by _{file_id}_ and inserts such data into a SQLite SQL table.

Additionally, analytics from two SQL queries can be retrieved through the following endpoint:
* **GET** /Query/{query_id}

  It executes a SELECT query from an SQL file identified by _{query_id}_, and retrieves the result in JSON format, row by row.

API logic is located in _main.py_ script.

Logic used to create the neccessary SQLite database and tables is located in _database.py_ script.
