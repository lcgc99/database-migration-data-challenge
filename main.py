from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import pandas as pd
import sqlite3

DATABASE_NAME = 'target_database.db'
COLUMN_NAMES = {
    'hired_employees': ['Id', 'Name', 'Datetime', 'DepartmentId', 'JobId'],
    'departments': ['Id', 'Department'],
    'jobs': ['Id', 'Job'],
}
BATCH_SIZE = 1000

app = FastAPI()

@app.get("/TestEndpoint")
async def root():
    return {"message": "starting the API development"}

@app.get("/")
async def read_root():
    return RedirectResponse("/docs")

@app.get("/Data/{file_id}")
async def get_data(file_id: str):

    # Use Pandas to read the CSV data
    df = pd.read_csv(f'{file_id}.csv', header=None, dtype="string")

    # Convert DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')

    return {"data": data}

@app.post("/Upload/{file_id}")
async def upload_data(file_id: str, skip: int = 0):

    df = pd.read_csv(f'{file_id}.csv', header=None, dtype="string")
    df.columns = COLUMN_NAMES[file_id]

    with sqlite3.connect(DATABASE_NAME) as conn:
        df.iloc[skip:].to_sql(
            # SQL doesn't consider case but Python does
            name=str.upper(file_id),
            con=conn,
            if_exists='append',
            index=False,
            chunksize=BATCH_SIZE
        )