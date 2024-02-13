from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from io import BytesIO
import pandas as pd
from excelConverter import create_sankey_diagram

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), sheet_name: str = 'Sheet 1'):
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents), sheet_name=sheet_name)
        file_path = create_sankey_diagram(df)

        file_url = file_path.replace('static', '/static')  

        return {"redirect_url": f"http://192.168.1.8:8080/view_sankey"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/view_sankey", response_class=HTMLResponse)
def view_sankey():
    return HTMLResponse(content=f"""
    <html>
        <head>
            <title>View Sankey Diagram</title>
        </head>
        <body>
            <h3>Click the button to view the Sankey Diagram</h3>
            <form action="http://192.168.1.8:8080/static/sankey_diagram.html">
                <input type="submit" value="View Sankey Diagram" />
            </form>
        </body>
    </html>
    """, status_code=200)

@app.get("/")
def read_root():
    return {"message": "Upload your xlsx file here"}

