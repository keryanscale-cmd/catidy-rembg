from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rembg import remove, new_session
from PIL import Image
import base64
import io

app = FastAPI()
session = new_session("u2netp")

class ImageRequest(BaseModel):
    image_base64: str
    output_format: str = "PNG"

class ImageResponse(BaseModel):
    image_base64: str
    success: bool

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/remove-background", response_model=ImageResponse)
def remove_background(request: ImageRequest):
    try:
        b64 = request.image_base64
        if "," in b64:
            b64 = b64.split(",")[1]
        image_bytes = base64.b64decode(b64)
        input_image = Image.open(io.BytesIO(image_bytes))
        output_image = remove(input_image, session=session)
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_b64 = base64.b64encode(output_buffer.getvalue()).decode("utf-8")
        return ImageResponse(
            image_base64=f"data:image/png;base64,{output_b64}",
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
