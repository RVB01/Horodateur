from PIL import Image, ImageFont, ImageDraw
import pathlib
import os
import datetime

dossier_local = pathlib.Path(__file__).parent
dossier_timestamp = dossier_local / "Horodaté"
dossier_timestamp.mkdir(exist_ok=True)
dossier = [f for f in dossier_local.iterdir() if f.is_file() and f is not __file__]
for photo in dossier:
    date_unix = os.path.getmtime(photo)
    date_modif = datetime.datetime.fromtimestamp(date_unix)
    texte = str(date_modif)
    img = Image.open(photo)
    police = ImageFont.truetype("calibri.ttf", 60)
    date = ImageDraw.Draw(img)
    larg, haut = img.size
    position = (larg*0.85, haut*0.96)
    bbox = date.textbbox(position, texte, font=police)
    date.rectangle(bbox, fill="black")
    date.text(position, f"{texte}", font=police, fill=(255,255,255))
    try:
        img.save(dossier_timestamp / photo.name)
    except:
        pass
