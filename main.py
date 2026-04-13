import os
import io
import google.generativeai as genai
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from PIL import Image

app = FastAPI()

# index.html қайда тұрғанын тексер. Егер негізгі бетте болса "." қалдыр
templates = Jinja2Templates(directory=".")

# API Key
genai.configure(api_key="AIzaSyA7O2n8B-yyF7WdNKJIcpYPfNL4fvrzP2k")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        return templates.TemplateResponse(request=request, name="index.html")
    except Exception as e:
        return HTMLResponse(content=f"HTML табылмады: {str(e)}", status_code=404)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        content = await file.read()
        img = Image.open(io.BytesIO(content))
        
        # Модельді дұрыс шақыру
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([
            "Суреттегі барлық қолтаңба жазуларды оқы. Тек жазылған мәтінді ғана жаз, басқа ештеңе жазба.",
            img
        ])
        
        return {"text": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"text": f"Gemini қатесі: {str(e)}"})
