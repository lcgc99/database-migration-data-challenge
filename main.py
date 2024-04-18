from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/testendpoint")
async def root():
    return {"message": "starting the API development"}

@app.get("/Data/{file_id}")
async def get_data(file_id: str):

    # Use Pandas to read the CSV data
    df = pd.read_csv(file_id, header=None, dtype="string")

    # Convert DataFrame to a list of dictionaries (if needed)
    data = df.to_dict(orient='records')

    return {"data": data}