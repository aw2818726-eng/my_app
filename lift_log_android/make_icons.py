"""Replace the default Capacitor launcher icons with the Lift Log icon.

Run after `npx cap add android`. Uses plain (non-adaptive) icons so it does not
depend on the adaptive icon XML layout: the adaptive icon folder is removed.
"""
import os, shutil
from PIL import Image, ImageDraw

res = os.path.join("android", "app", "src", "main", "res")
src = Image.open(os.path.join("www", "icon_512.png")).convert("RGBA")
sizes = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}

for dens, px in sizes.items():
    d = os.path.join(res, "mipmap-" + dens)
    os.makedirs(d, exist_ok=True)
    sq = src.resize((px, px), Image.LANCZOS)
    sq.save(os.path.join(d, "ic_launcher.png"))
    mask = Image.new("L", (px * 4, px * 4), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, px * 4 - 1, px * 4 - 1], fill=255)
    mask = mask.resize((px, px), Image.LANCZOS)
    rd = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    rd.paste(sq, (0, 0), mask)
    rd.save(os.path.join(d, "ic_launcher_round.png"))
    fg = os.path.join(d, "ic_launcher_foreground.png")
    if os.path.exists(fg):
        os.remove(fg)

anydpi = os.path.join(res, "mipmap-anydpi-v26")
if os.path.isdir(anydpi):
    shutil.rmtree(anydpi)
print("icons replaced")
