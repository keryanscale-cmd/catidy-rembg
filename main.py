from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
from rembg import remove
from PIL import Image
import io

app = FastAPI()

class ImageRequest(BaseModel):
    image_base64: str  # data:image/jpeg;base64,... ou juste le base64 pur
    output_format: str = "PNG"  # toujours PNG pour conserver la transparence

class ImageResponse(BaseModel):
    image_base64: str  # data:image/png;base64,...
    success: bool

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/remove-background", response_model=ImageResponse)
def remove_background(request: ImageRequest):
    try:
        # Nettoyer le base64 (enlever le préfixe data:image/...;base64,)
        b64 = request.image_base64
        if "," in b64:
            b64 = b64.split(",")[1]

        # Décoder
        image_bytes = base64.b64decode(b64)

        # Détourage avec rembg
        input_image = Image.open(io.BytesIO(image_bytes))
        output_image = remove(input_image)

        # Encoder en PNG (transparence conservée)
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_b64 = base64.b64encode(output_buffer.getvalue()).decode("utf-8")

        return ImageResponse(
            image_base64=f"data:image/png;base64,{output_b64}",
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
