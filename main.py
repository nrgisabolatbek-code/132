import google.generativeai as genai
from IPython.display import Javascript
from google.colab.output import eval_js
from base64 import b64decode
from google.colab import files
import PIL.Image
import io

genai.configure(api_key="AIzaSyA7O2n8B-yYf7WdNKJIcpYPfNL4fvrzP2k")

def take_photo():
    js = Javascript('''
        async function takePhoto() {
            const div = document.createElement('div');
            const capture = document.createElement('button');
            capture.textContent = '📸 Суретке түсір';
            capture.style.fontSize = '20px';
            capture.style.padding = '10px 20px';
            capture.style.margin = '10px';
            capture.style.cursor = 'pointer';
            capture.style.backgroundColor = '#4CAF50';
            capture.style.color = 'white';
            capture.style.border = 'none';
            capture.style.borderRadius = '8px';
            const video = document.createElement('video');
            video.style.display = 'block';
            video.style.width = '100%';
            const stream = await navigator.mediaDevices.getUserMedia({video: true});
            document.body.appendChild(div);
            div.appendChild(video);
            div.appendChild(capture);
            video.srcObject = stream;
            await video.play();
            await new Promise((resolve) => capture.onclick = resolve);
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            stream.getTracks().forEach(track => track.stop());
            div.remove();
            return canvas.toDataURL('image/jpeg', 0.9);
        }
        takePhoto()
    ''')
    data = eval_js(js.data)
    binary = b64decode(data.split(',')[1])
    image = PIL.Image.open(io.BytesIO(binary))
    print("✅ Сурет түсірілді!")
    return image

# 1. Суретке түс
image = take_photo()

# 2. Gemini арқылы тану
model = genai.GenerativeModel("gemini-flash-latest")
response = model.generate_content([
    image,
    "Суреттегі барлық қолтаңба жазуларды оқы. Тек жазылған мәтінді ғана жаз, басқа ештеңе жазба."
])

tanylgan_matn = response.text

# 3. Экранға шығар
print("✅ Танылған мәтін:")
print("-" * 40)
print(tanylgan_matn)

# 4. TXT файл жасап жүктеу
with open("natije.txt", "w", encoding="utf-8") as f:
    f.write(tanylgan_matn)

files.download("natije.txt")
print("✅ natije.txt файлы жүктелді!")
