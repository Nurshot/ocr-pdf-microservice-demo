from fastapi import FastAPI, UploadFile, File, Form
import os
import base64
from rpc_client import OcrRpcClient

app = FastAPI()

@app.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    temp_file_path = file.filename
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    ocr_rpc = OcrRpcClient()
    

    with open(temp_file_path, "rb") as buffer:
        file_data = buffer.read()
        file_base64 = base64.b64encode(file_data).decode('utf-8')

    request_json = {
        'file': file_base64,
    }


    response = ocr_rpc.call(request_json)

    os.remove(temp_file_path)

    return response
