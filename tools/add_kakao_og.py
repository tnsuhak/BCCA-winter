from pathlib import Path
import base64
import io
import re
from PIL import Image

ROOT = Path('.')
INDEX = ROOT / 'index.html'
OUT = ROOT / 'assets' / 'carney-og.jpg'
OLD = 'https://bcca-winter.netlify.app'
NEW = 'https://carney-winter.netlify.app'


def choose_page_photo(html: str):
    candidates = []
    for m in re.finditer(r'data:image/(jpeg|jpg|png|webp);base64,([A-Za-z0-9+/=\s]+)', html, re.I):
        raw = re.sub(r'\s+', '', m.group(2))
        try:
            data = base64.b64decode(raw, validate=False)
            im = Image.open(io.BytesIO(data))
            im.load()
        except Exception:
            continue
        w, h = im.size
        if w < 640 or h < 360:
            continue
        ratio = w / h
        context = html[max(0, m.start()-900):min(len(html), m.end()+900)].lower()
        score = min((w*h)/250000, 30)
        if 1.25 <= ratio <= 2.4:
            score += 22
        elif 1.0 <= ratio <= 3.0:
            score += 8
        else:
            score -= 15
        for kw, pts in [
            ('carney', 45), ('archbishop', 35), ('school', 24), ('학교', 24),
            ('campus', 18), ('학생', 8), ('student', 8), ('vancouver', 8),
            ('canada', 8), ('캐나다', 8), ('hero', 12), ('school-photo', 20),
        ]:
            if kw in context:
                score += pts
        for kw, pts in [
            ('카톡', 80), ('후기', 60), ('review', 60), ('schedule', 55), ('일정', 55),
            ('logo', 70), ('favicon', 70), ('qr', 60), ('instagram', 45), ('reel', 45),
            ('kakao', 60), ('map', 25), ('brochure', 20),
        ]:
            if kw in context:
                score -= pts
        candidates.append((score, w*h, m.start(), im.copy().convert('RGB'), w, h, context[:220]))

    if not candidates:
        return None, []
    candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return candidates[0], candidates[:10]


def crop_og(im: Image.Image) -> Image.Image:
    target_ratio = 1200 / 630
    w, h = im.size
    ratio = w / h
    if ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        im = im.crop((left, 0, left + new_w, h))
    elif ratio < target_ratio:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        im = im.crop((0, top, w, top + new_h))
    return im.resize((1200, 630), Image.Resampling.LANCZOS)


def remove_social_meta(html: str) -> str:
    meta_re = re.compile(
        r'<meta\b(?=[^>]*(?:property|name)\s*=\s*["\'](?:og:|twitter:)[^"\']*["\'])[^>]*>\s*',
        re.I,
    )
    return meta_re.sub('', html)


def add_social_meta(html: str, title: str, desc: str, url: str, image_url: str) -> str:
    html = remove_social_meta(html)
    tags = (
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:locale" content="ko_KR">\n'
        f'<meta property="og:site_name" content="TNS유학 · EduSmart">\n'
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{desc}">\n'
        f'<meta property="og:url" content="{url}">\n'
        f'<meta property="og:image" content="{image_url}">\n'
        f'<meta property="og:image:secure_url" content="{image_url}">\n'
        f'<meta property="og:image:type" content="image/jpeg">\n'
        f'<meta property="og:image:width" content="1200">\n'
        f'<meta property="og:image:height" content="630">\n'
        f'<meta property="og:image:alt" content="2027 Archbishop Carney 캐나다 밴쿠버 겨울 스쿨링">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{title}">\n'
        f'<meta name="twitter:description" content="{desc}">\n'
        f'<meta name="twitter:image" content="{image_url}">\n'
    )
    head = re.search(r'<head\b[^>]*>', html, re.I)
    if not head:
        raise SystemExit('No <head> found')
    return html[:head.end()] + '\n' + tags + html[head.end():]


html = INDEX.read_text(encoding='utf-8')
html = html.replace(OLD, NEW).replace('http://bcca-winter.netlify.app', NEW)
chosen, top = choose_page_photo(html)
if chosen is None:
    raise SystemExit('No suitable embedded site photo found; refusing to reuse the old BCCA OG image.')
score, _, pos, image, w, h, _ = chosen
OUT.parent.mkdir(parents=True, exist_ok=True)
crop_og(image).save(OUT, format='JPEG', quality=88, optimize=True, progressive=True)
print(f'Chosen existing page image at byte {pos}: {w}x{h}, score={score:.1f}')
for i, c in enumerate(top[:5], 1):
    print(f'candidate {i}: score={c[0]:.1f}, size={c[4]}x{c[5]}, byte={c[2]}')

main_title = '2027 캐나다 밴쿠버 겨울 스쿨링 | Archbishop Carney'
main_desc = '미서부 투어 5일 + Archbishop Carney 정규수업 4주 + 홈스테이 + 온라인 ESL/MATH · 중1~고1 · 소수 정원 13~14명'
image_url = NEW + '/assets/carney-og.jpg?v=20260910'
html = add_social_meta(html, main_title, main_desc, NEW + '/', image_url)
INDEX.write_text(html, encoding='utf-8')

video = ROOT / 'student-life-videos.html'
if video.exists():
    v = video.read_text(encoding='utf-8').replace(OLD, NEW).replace('http://bcca-winter.netlify.app', NEW)
    v = add_social_meta(
        v,
        '2027 Carney 겨울 스쿨링 실제 학생 생활 영상',
        '홈스테이·오리엔테이션·식사·주말 활동 등 EduSmart 학생들의 실제 캐나다 생활 영상을 확인하세요.',
        NEW + '/student-life-videos.html',
        image_url,
    )
    video.write_text(v, encoding='utf-8')

for name in ('sitemap.xml', 'robots.txt'):
    p = ROOT / name
    if p.exists():
        p.write_text(p.read_text(encoding='utf-8').replace(OLD, NEW).replace('http://bcca-winter.netlify.app', NEW), encoding='utf-8')

# Guardrails for Kakao/Open Graph and the renamed Netlify domain.
final = INDEX.read_text(encoding='utf-8')
required = [
    '<meta property="og:image" content="https://carney-winter.netlify.app/assets/carney-og.jpg?v=20260910">',
    '<meta property="og:title" content="2027 캐나다 밴쿠버 겨울 스쿨링 | Archbishop Carney">',
    '<meta property="og:url" content="https://carney-winter.netlify.app/">',
]
for needle in required:
    if needle not in final:
        raise SystemExit(f'Missing required tag: {needle}')
if 'bcca-winter.netlify.app' in final:
    raise SystemExit('Old Netlify domain remains in index.html')
print('Kakao/Open Graph metadata and Carney domain migration complete.')
