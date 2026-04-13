import os
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from PIL import Image
import io

app = FastAPI()

# Түзету: Мұнда папканы дұрыс көрсету маңызды
templates = Jinja2Templates(directory=".")

genai.configure(api_key="AIzaSyA7O2n8B-yyF7WdNKJIcpYPfNL4fvrzP2k")
model = genai.GenerativeModel("gemini-1.5-flash")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # ТҮЗЕТІЛГЕН ЖОЛ:
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    request_object_content = await file.read()
    img = Image.open(io.BytesIO(request_object_content))
    
    response = model.generate_content([
        "Суреттегі барлық қолтаңба жазуларды оқы. Тек жазылған мәтінді ғана жаз, басқа ештеңе жазба.",
        img
    ])
    
    return {"text": response.text}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
