from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
NAVY = (10, 39, 66)
NAVY2 = (20, 66, 94)
GOLD = (240, 178, 56)
CREAM = (248, 245, 238)
WHITE = (255, 255, 255)
MUTED = (208, 222, 232)

font_b = '/usr/share/fonts/truetype/nanum/NanumSquareB.ttf'
font_r = '/usr/share/fonts/truetype/nanum/NanumSquareR.ttf'
if not os.path.exists(font_r):
    font_r = '/usr/share/fonts/truetype/nanum/NanumSquareRoundR.ttf'
if not os.path.exists(font_b):
    raise SystemExit('Nanum font not found')

img = Image.new('RGB', (W, H), NAVY)
d = ImageDraw.Draw(img)
d.polygon([(840, 0), (1200, 0), (1200, 630), (700, 630)], fill=NAVY2)
d.ellipse([930, -100, 1260, 230], fill=(25, 78, 108))
d.ellipse([1020, 20, 1220, 220], outline=GOLD, width=8)
d.rectangle([74, 74, 160, 82], fill=GOLD)

f_top = ImageFont.truetype(font_b, 28)
f_eng = ImageFont.truetype(font_b, 61)
f_kr = ImageFont.truetype(font_b, 50)
f_pill = ImageFont.truetype(font_b, 26)
f_small = ImageFont.truetype(font_r, 24)
f_brand = ImageFont.truetype(font_b, 26)

d.text((74, 100), '2027 WINTER SCHOOLING · VANCOUVER, CANADA', font=f_top, fill=GOLD)
d.text((74, 170), 'Archbishop', font=f_eng, fill=WHITE)
d.text((74, 242), 'Carney', font=f_eng, fill=WHITE)
d.text((74, 338), '캐나다 밴쿠버 겨울 스쿨링', font=f_kr, fill=WHITE)

def pill(x, y, w, h, text):
    d.rounded_rectangle([x, y, x+w, y+h], radius=14, fill=CREAM)
    box = d.textbbox((0, 0), text, font=f_pill)
    tx = x + (w - (box[2]-box[0])) / 2
    ty = y + (h - (box[3]-box[1])) / 2 - 2
    d.text((tx, ty), text, font=f_pill, fill=NAVY)

pill(74, 430, 360, 58, '미서부 5일 + 정규수업 4주')
pill(450, 430, 300, 58, '중1~고1 · 13~14명')

d.rounded_rectangle([844, 284, 1126, 466], radius=24, outline=(78, 125, 151), width=2)
d.text((882, 320), 'ARCHBISHOP', font=ImageFont.truetype(font_b, 26), fill=MUTED)
d.text((882, 362), 'CARNEY', font=ImageFont.truetype(font_b, 37), fill=WHITE)
d.multiline_text((882, 412), 'REGIONAL\nSECONDARY SCHOOL', font=ImageFont.truetype(font_b, 18), fill=MUTED, spacing=5)
d.text((74, 550), 'TNS유학 · EduSmart', font=f_brand, fill=MUTED)
d.text((872, 550), '2027.01.13 — 02.13', font=f_small, fill=MUTED)

Path('assets').mkdir(exist_ok=True)
img.save('assets/carney-og.jpg', 'JPEG', quality=90, optimize=True, progressive=True)
img.save('og.jpg', 'JPEG', quality=90, optimize=True, progressive=True)
print('Built 1200x630 Carney Open Graph image and replaced stale BCCA og.jpg')
