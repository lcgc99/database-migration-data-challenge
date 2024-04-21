import sqlite3
import pandas as pd
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse

DATABASE_NAME = 'target_database.db'
COLUMN_NAMES = {
    'hired_employees': ['Id', 'Name', 'Datetime', 'DepartmentId', 'JobId'],
    'departments': ['Id', 'Department'],
    'jobs': ['Id', 'Job'],
}
BATCH_LIMIT = 1000

app = FastAPI()


@app.get("/")
async def read_root():
    return RedirectResponse("/docs")


@app.get("/Data/{file_id}")
async def get_data(file_id: str):
    """
    This endpoint is used to display data from the file specified.

    Args:
        file_id (str): Name of the file from which data is retrieved.
            Must be one of the following values: 'hired_employees', 'departments', 'jobs'.

    Returns:
        dict: Dictionary containing all data from the file specified in file_id

    Raises:
        404 Not Found: If file_id is not valid
    """
    try:
        df = pd.read_csv(f'{file_id}.csv', header=None, dtype="string")
        data = df.to_dict(orient='records')

        return {"data": data}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/Upload/{file_id}")
async def upload_data(file_id: str, skip: int = 0):
    """
    This endpoint is used to insert data from the file specified into a table
    from a SQLite database which name is stored in DATABASE_NAME.

    Args:
        file_id (str): Name of the file from which data is retrieved.
            Must be one of the following values: 'hired_employees', 'departments', 'jobs'.
        skip (int, optional): Number of records to be skipped when inserting data.
            As the maximum batch size is 1000, it is important to loop this parameter
            to avoid a primary key constraint failure. Defaults to 0.

    Returns:
        None

    Raises:
        409 Not found: If file_id is not valid.
        409 Conflict: If rows were already inserted into the table.
    """
    try:
        df = pd.read_csv(f'{file_id}.csv', header=None, dtype="string")
        df.columns = COLUMN_NAMES[file_id]

        with sqlite3.connect(DATABASE_NAME) as conn:
            df.iloc[skip: skip + BATCH_LIMIT].to_sql(
                name=str.upper(file_id),
                con=conn,
                if_exists='append',
                index=False,
            )

        return Response(status_code=204)

    except Exception as e:
        if 'No such file or directory' in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=409, detail=str(e))


@app.get("/Query/{query_id}")
async def query(query_id: str):
    """
    This endpoint is used to retrieve results from the execution of SQL queries.

    Args:
        query_id (str): Name of the SQL query to be executed.
            Must be one of the following values:
            1. EmployeesHiredByJobANDDepartment2021Quarters
            2. EmployeesHiredByDepartment2021

    Returns:
        results (list): List containing the results of the query row by row.

    Raises:
        404 Not Found: If the name of the query is not found in the system.
    """
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            file = open(f'{query_id}.sql', 'r')
            conn = sqlite3.connect(DATABASE_NAME)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(file.read())
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            conn.close()

        return result

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
