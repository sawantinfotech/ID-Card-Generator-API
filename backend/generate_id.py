from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, IDCard
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from io import BytesIO

router = APIRouter(tags=["ID Generator"])

OUTPUT_DIR = "generated_cards"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/generate-id")
async def generate_id_card(
    name: str = Form(...),
    output_format: str = Form(...),  # "image" or "pdf"
    api_key: str = Form(...),
    api_secret: str = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(api_key=api_key, api_secret=api_secret).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API credentials")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{user.username}_{timestamp}"

    # Save the uploaded photo temporarily
    photo_path = f"{OUTPUT_DIR}/{file_name}_photo.jpg"
    with open(photo_path, "wb") as f:
        f.write(await photo.read())

    if output_format == "image":
        final_path = f"{OUTPUT_DIR}/{file_name}.png"
        create_image_card(name, photo_path, final_path)
    elif output_format == "pdf":
        final_path = f"{OUTPUT_DIR}/{file_name}.pdf"
        create_pdf_card(name, photo_path, final_path)
    else:
        raise HTTPException(status_code=400, detail="Invalid output format")

    # Store in DB
    card = IDCard(
        name=name,
        user_id=user.id,
        output_format=output_format,
        file_path=final_path
    )
    db.add(card)
    db.commit()

    return {
        "message": "ID card generated successfully",
        "file_path": final_path
    }

def create_image_card(name, photo_path, output_path):
    base = Image.new("RGB", (600, 300), "white")
    draw = ImageDraw.Draw(base)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    draw.text((20, 20), f"Name: {name}", font=font, fill="black")
    
    photo = Image.open(photo_path).resize((100, 100))
    base.paste(photo, (20, 60))

    base.save(output_path)

def create_pdf_card(name, photo_path, output_path):
    c = canvas.Canvas(output_path, pagesize=(300, 150))
    c.drawString(30, 120, f"Name: {name}")
    c.drawImage(photo_path, 30, 20, width=60, height=60)
    c.save()
