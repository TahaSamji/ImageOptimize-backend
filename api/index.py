from fastapi import FastAPI,UploadFile
from fastapi.responses import FileResponse
import resmushit
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
import os
UPLOAD_DIR = Path() / 'uploads'
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadfile")
async def read(file_upload:UploadFile):
    file_name = file_upload.filename
    _, file_extension = os.path.splitext(file_name)
    file_extension = file_extension[1:]
    
    print(f"File Extension: {file_extension}")
    data = await file_upload.read()
    save_to = UPLOAD_DIR / file_name
    with open(save_to,'wb') as f:
        f.write(data)

    resmushit.from_path(image_path="".join(["uploads/",file_name]),quality=95,output_dir='output/',preserve_filename=True)
    print("success")
    return FileResponse(path="".join(["output/",file_name]), filename=file_name, media_type=''.join(["image/",file_extension]))



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app,host="0.0.0.0",port=8000)