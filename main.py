from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from io import BytesIO
import pandas as pd
from excelConverter import create_sankey_diagram

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), sheet_name: str = 'Sheet 1'):
    try:
        #read file into memory
        contents = await file.read()

        # using BytesIO
        df = pd.read_excel(BytesIO(contents), sheet_name=sheet_name)
        
        # call create_sankey_diagram(
        fig = create_sankey_diagram(df)

        # translate to html
        fig.write_html("sankey_diagram.html")

        return HTMLResponse(content="<html><body><h1>Sankey chart was created</h1></body></html>", status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Upload your xlsx file here"}
