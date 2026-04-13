import os
import io
import google.generativeai as genai
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from PIL import Image

app = FastAPI()
templates = Jinja2Templates(directory=".")

API_KEY = "AIzaSyBQBTNk3l18J3mFj4scTRUnK-WZcLYxjEY"
genai.configure(api_key=API_KEY)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        content = await file.read()
        img = Image.open(io.BytesIO(content))
        
        # Модельді жаңаша шақыру
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        response = model.generate_content([
            "Суреттегі барлық қолтаңба жазуларды оқы. Тек жазылған мәтінді ғана жаз, басқа ештеңе жазба.",
            img
        ])
        
        return {"text": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"text": f"Gemini қатесі: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
