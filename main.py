from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from PIL import Image
import io
from datetime import datetime
from text_manipulation import *


app = FastAPI()
TEMP_FOLDER = "temp"
IMAGES_FOLDER = "img"

# Add folders to an app
app.mount("/img", StaticFiles(directory=IMAGES_FOLDER), name="img")

@app.get("/send")
def send_photo(request: Request):
    ok = request.query_params.get("ok")
    message_html = ""

    if ok == "1":
        message_html = '<p style="color: green;">✅ Plik zapisany pomyślnie!</p>'
    elif ok == "0":
        message_html = '<p style="color: red;">❌ Wystąpił błąd podczas zapisu pliku.</p>'

    return HTMLResponse(f"""
    <html>
        <body>
            {message_html}
            <h2>Wyślij zdjęcie</h2>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept="image/*" capture="camera">
                <input type="submit" value="Wyślij">
            </form>
        </body>
    </html>
""")

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Turn image black-white and save it to img folder
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        bl_img = img.convert("L")

        timestamp = datetime.now().strftime("%d%m%Y%H%M")
        file_path = os.path.join(IMAGES_FOLDER, f"img_{timestamp}.png")
        bl_img.save(file_path, format="PNG")

        return RedirectResponse(url="/send?ok=1", status_code=303)
    
    except Exception as e:
        print("Error: ", e)
        return RedirectResponse(url="/send?ok=0", status_code=303)
    
@app.get("/transcribe")
def transcribe():
    images = [f for f in os.listdir(IMAGES_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    # Generate HTLM
    html_images = ""
    for img in images:
        html_images += f'<img src="/img/{img}" width="200" class="selectable" onclick="selectImage(this)" data-filename="{img}">'

    return HTMLResponse(f"""
    <html>
    <head>
        <style>
            body {{
                font-family: sans-serif;
                text-align: center;
            }}
            .selectable {{
                margin: 10px;
                border: 3px solid transparent;
                cursor: pointer;
                transition: border 0.2s;
            }}
            .selected {{
                border: 3px solid blue;
            }}
            #confirm-btn {{
                background-color: green;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                font-size: 16px;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <form id="process-form" action="/process" method="post">
            <input type="hidden" name="filename" id="filename-input">
            <button type="button" id="confirm-btn" onclick="confirmSelection()">Potwierdź</button>
        </form>
        <div id="image-container">
            {html_images}
        </div>

        <script>
            let selectedImage = null;

            function selectImage(img) {{
                if (selectedImage) {{
                    selectedImage.classList.remove("selected");
                }}
                img.classList.add("selected");
                selectedImage = img;
            }}

            function confirmSelection() {{
                if (!selectedImage) {{
                    alert("Nie wybrano żadnego obrazu!");
                    return;
                }}
                const filename = selectedImage.getAttribute("data-filename");
                document.getElementById("filename-input").value = filename;
                document.getElementById("process-form").submit();
            }}
        </script>
    </body>
    </html>
    """)

@app.post("/process", response_class=HTMLResponse)
async def processs(filename: str = Form(...)):
    """
    Processing pipeline. Extract text -> Sanitize output -> Analyze with LLM -> ...
    """
    print(f"Wybrano plik: {filename}")

    # Choose a file
    file = os.path.join(IMAGES_FOLDER, filename)
    # Extract text from a file
    text_ = extract_text(file)
    # Process text 
    text_= process_text(text_)
    # Extract norwegian texts from whole text
    norwegian_data = analyze_text(text_) # dict - {'words': [], 'sentences': []}


    return HTMLResponse(f"""
    <html>
        <body style="font-family: sans-serif; text-align: center;">
            <h1>Wybrano plik:</h1>
            <p>{filename}</p>
            <img src="/img/{filename}" style="max-width:300px;">
            <br><br>
            {norwegian_data}
            <br>
            <a href="/transcribe">Wróć</a>
        </body>
    </html>
    """)

if __name__ == "__main__":
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    os.makedirs(IMAGES_FOLDER, exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)  
