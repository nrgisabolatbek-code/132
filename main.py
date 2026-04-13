import os
import io
import google.generativeai as genai
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from PIL import Image

app = FastAPI()

# HTML файлының орналасқан жері (негізгі папка)
templates = Jinja2Templates(directory=".")

# Сенің жаңа API кілтің
API_KEY = "AIzaSyBQBTNk3l18J3mFj4scTRUnK-WZcLYxjEY"
genai.configure(api_key=API_KEY)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        return templates.TemplateResponse(request=request, name="index.html")
    except Exception as e:
        return HTMLResponse(content=f"Қате: index.html файлы табылмады. {str(e)}", status_code=404)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Суретті оқу
        request_object_content = await file.read()
        img = Image.open(io.BytesIO(request_object_content))
        
        # Gemini моделін іске қосу
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Мәтінді тануға сұраныс жіберу
        response = model.generate_content([
            "Суреттегі барлық қолтаңба жазуларды оқы. Тек жазылған мәтінді ғана жаз, басқа ештеңе жазба.",
            img
        ])
        
        # Егер жауап келсе, мәтінді жіберу
        return {"text": response.text}
        
    except Exception as e:
        # Қате болса, оның себебін экранға шығару
        return JSONResponse(
            status_code=500, 
            content={"text": f"Gemini қатесі: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    # Railway-де порт автоматты түрде беріледі
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
