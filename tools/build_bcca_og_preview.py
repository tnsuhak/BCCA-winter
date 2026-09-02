from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = Path('og-bcca-2027.jpg')
HTML = Path('index.html')

navy = '#0E2A47'
navy2 = '#17395E'
red = '#C94A3F'
gold = '#B99750'
white = '#FFFFFF'
cream = '#F7F3EA'

font_candidates = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
]
font_path = next((p for p in font_candidates if os.path.exists(p)), None)
if not font_path:
    raise SystemExit('Noto CJK font not found')

def F(size):
    return ImageFont.truetype(font_path, size=size)

img = Image.new('RGB', (W, H), cream)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 18], fill=navy)
d.rectangle([0, H-72, W, H], fill=navy)
d.rounded_rectangle([825, 60, 1150, 520], radius=34, fill=navy2)
d.ellipse([900, 125, 1075, 300], fill=red)

# Stylised maple leaf emblem
cx, cy = 988, 214
pts = [
    (cx, cy-78),(cx+22, cy-36),(cx+55, cy-49),(cx+42, cy-13),
    (cx+84, cy-4),(cx+44, cy+23),(cx+59, cy+60),(cx+17, cy+44),
    (cx, cy+88),(cx-17, cy+44),(cx-59, cy+60),(cx-44, cy+23),
    (cx-84, cy-4),(cx-42, cy-13),(cx-55, cy-49),(cx-22, cy-36)
]
d.polygon(pts, fill=white)

d.rounded_rectangle([68, 62, 340, 112], radius=18, fill=red)
d.text((91, 72), '2027 캐나다 겨울방학', font=F(27), fill=white)
d.text((68, 142), 'BCCA 겨울 스쿨링', font=F(66), fill=navy)
d.text((68, 232), '정규수업 4주 + 미서부 4박5일', font=F(34), fill=red)
d.line([68, 294, 770, 294], fill=gold, width=3)
d.text((68, 320), '영어캠프가 아니라,', font=F(31), fill=navy)
d.text((68, 363), '캐나다 학교에서 4주간 실제 수업에 참여합니다.', font=F(31), fill=navy)

facts = [
    ('기간', '2027. 1. 13 ~ 2. 13'),
    ('대상', '초5 ~ 고1 · 총 20명'),
    ('구성', 'BCCA 정규수업 + 홈스테이 + 방과후 영어·수학'),
]
y = 430
for label, value in facts:
    d.rounded_rectangle([68, y, 146, y+38], radius=12, fill=navy)
    d.text((90, y+5), label, font=F(20), fill=white)
    d.text((165, y+2), value, font=F(24), fill=navy)
    y += 49

d.text((885, 337), 'VANCOUVER', font=F(26), fill=white)
d.text((913, 374), 'CANADA', font=F(22), fill='#DDE7F1')
d.text((872, 435), '2027 BCCA', font=F(25), fill=white)
d.text((859, 470), 'WINTER SCHOOLING', font=F(18), fill='#DDE7F1')
d.text((68, 574), 'TNS유학', font=F(30), fill=white)
d.text((198, 580), '캐나다 겨울 스쿨링 가이드', font=F(19), fill='#DDE7F1')
d.text((923, 580), '상담 010-5150-0105', font=F(19), fill=white)

img.save(OUT, 'JPEG', quality=86, optimize=True)
if Image.open(OUT).size != (1200, 630):
    raise SystemExit('OG image dimension validation failed')

html = HTML.read_text(encoding='utf-8')
preview_image = 'https://deploy-preview-3--bcca-winter.netlify.app/og-bcca-2027.jpg'
old_og = '<meta property="og:image" content="https://bcca-winter.netlify.app/og.jpg">'
new_og = '\n'.join([
    f'<meta property="og:image" content="{preview_image}">',
    f'<meta property="og:image:secure_url" content="{preview_image}">',
    '<meta property="og:image:type" content="image/jpeg">',
    '<meta property="og:image:width" content="1200">',
    '<meta property="og:image:height" content="630">',
])
if old_og in html:
    html = html.replace(old_og, new_og, 1)
elif preview_image not in html:
    raise SystemExit('Expected current og:image tag not found')

old_tw = '<meta name="twitter:image" content="https://bcca-winter.netlify.app/og.jpg">'
new_tw = f'<meta name="twitter:image" content="{preview_image}">'
if old_tw in html:
    html = html.replace(old_tw, new_tw, 1)
elif new_tw not in html:
    raise SystemExit('Expected current twitter:image tag not found')

HTML.write_text(html, encoding='utf-8')
print(f'Built {OUT} ({OUT.stat().st_size} bytes) and updated preview OG metadata')
