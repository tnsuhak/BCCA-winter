from pathlib import Path
import base64
import io
import re
import urllib.request
from urllib.parse import urljoin
from PIL import Image

ROOT = Path('.')
INDEX = ROOT / 'index.html'
OUT = ROOT / 'assets' / 'carney-og.jpg'
OLD = 'https://bcca-winter.netlify.app'
NEW = 'https://carney-winter.netlify.app'

BAD = [('카톡', 90), ('후기', 70), ('review', 70), ('schedule', 60), ('일정', 60),
       ('logo', 80), ('favicon', 80), ('qr', 70), ('instagram', 50), ('reel', 50),
       ('kakao', 70), ('map', 30), ('brochure', 25)]
GOOD = [('carney', 50), ('archbishop', 40), ('school', 28), ('학교', 28), ('campus', 22),
        ('학생', 10), ('student', 10), ('vancouver', 10), ('canada', 10), ('캐나다', 10),
        ('hero', 18), ('school-photo', 24), ('학교 전경', 30), ('전경', 18)]


def decode_src(src: str):
    try:
        if src.startswith('data:image/'):
            if ';base64,' not in src:
                return None
            raw = src.split(';base64,', 1)[1]
            data = base64.b64decode(re.sub(r'\s+', '', raw), validate=False)
        elif src.startswith('http://') or src.startswith('https://'):
            req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read(12_000_000)
        else:
            clean = src.split('?', 1)[0].split('#', 1)[0].lstrip('/')
            p = ROOT / clean
            if not p.exists() or not p.is_file():
                return None
            data = p.read_bytes()
        im = Image.open(io.BytesIO(data))
        im.load()
        return im.copy().convert('RGB')
    except Exception as e:
        print(f'Could not load image {src[:120]!r}: {e}')
        return None


def choose_page_photo(html: str):
    candidates = []
    # Prefer actual <img> elements so surrounding alt/class text informs the score.
    for m in re.finditer(r'<img\b[^>]*>', html, re.I | re.S):
        tag = m.group(0)
        sm = re.search(r'\bsrc\s*=\s*(["\'])(.*?)\1', tag, re.I | re.S)
        if not sm:
            continue
        src = sm.group(2).strip()
        if not src or src.startswith('data:image/svg'):
            continue
        image = decode_src(src)
        if image is None:
            continue
        w, h = image.size
        if w < 640 or h < 360:
            continue
        ratio = w / h
        context = (html[max(0, m.start()-1200):min(len(html), m.end()+1200)] + ' ' + tag).lower()
        score = min((w*h)/250000, 32)
        if 1.25 <= ratio <= 2.4:
            score += 24
        elif 1.0 <= ratio <= 3.0:
            score += 8
        else:
            score -= 18
        for kw, pts in GOOD:
            if kw in context:
                score += pts
        for kw, pts in BAD:
            if kw in context:
                score -= pts
        candidates.append((score, w*h, m.start(), image, w, h, src[:180]))

    # Fallback for CSS/data URIs not contained in an img element.
    if not candidates:
        for m in re.finditer(r'data:image/(jpeg|jpg|png|webp);base64,([A-Za-z0-9+/=]+)', html, re.I):
            image = decode_src(m.group(0))
            if image is None:
                continue
            w, h = image.size
            if w < 640 or h < 360:
                continue
            ratio = w / h
            context = html[max(0, m.start()-1000):min(len(html), m.end()+1000)].lower()
            score = min((w*h)/250000, 32) + (20 if 1.25 <= ratio <= 2.4 else 0)
            for kw, pts in GOOD:
                if kw in context:
                    score += pts
            for kw, pts in BAD:
                if kw in context:
                    score -= pts
            candidates.append((score, w*h, m.start(), image, w, h, 'embedded data image'))

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
    return re.sub(
        r'<meta\b(?=[^>]*(?:property|name)\s*=\s*["\'](?:og:|twitter:)[^"\']*["\'])[^>]*>\s*',
        '', html, flags=re.I)


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
    raise SystemExit('No suitable current-site photo found; refusing to reuse the old BCCA OG image.')
score, _, pos, image, w, h, src = chosen
OUT.parent.mkdir(parents=True, exist_ok=True)
crop_og(image).save(OUT, format='JPEG', quality=88, optimize=True, progressive=True)
print(f'Chosen current-site image: {w}x{h}, score={score:.1f}, src={src}')
for i, c in enumerate(top[:8], 1):
    print(f'candidate {i}: score={c[0]:.1f}, size={c[4]}x{c[5]}, src={c[6]}')

main_title = '2027 캐나다 밴쿠버 겨울 스쿨링 | Archbishop Carney'
main_desc = '미서부 투어 5일 + Archbishop Carney 정규수업 4주 + 홈스테이 + 온라인 ESL/MATH · 중1~고1 · 소수 정원 13~14명'
image_url = NEW + '/assets/carney-og.jpg?v=20260910'
html = add_social_meta(html, main_title, main_desc, NEW + '/', image_url)
INDEX.write_text(html, encoding='utf-8')

video = ROOT / 'student-life-videos.html'
if video.exists():
    v = video.read_text(encoding='utf-8').replace(OLD, NEW).replace('http://bcca-winter.netlify.app', NEW)
    v = add_social_meta(v,
        '2027 Carney 겨울 스쿨링 실제 학생 생활 영상',
        '홈스테이·오리엔테이션·식사·주말 활동 등 EduSmart 학생들의 실제 캐나다 생활 영상을 확인하세요.',
        NEW + '/student-life-videos.html', image_url)
    video.write_text(v, encoding='utf-8')

for name in ('sitemap.xml', 'robots.txt'):
    p = ROOT / name
    if p.exists():
        p.write_text(p.read_text(encoding='utf-8').replace(OLD, NEW).replace('http://bcca-winter.netlify.app', NEW), encoding='utf-8')

final = INDEX.read_text(encoding='utf-8')
for needle in [
    '<meta property="og:image" content="https://carney-winter.netlify.app/assets/carney-og.jpg?v=20260910">',
    '<meta property="og:title" content="2027 캐나다 밴쿠버 겨울 스쿨링 | Archbishop Carney">',
    '<meta property="og:url" content="https://carney-winter.netlify.app/">',
]:
    if needle not in final:
        raise SystemExit(f'Missing required tag: {needle}')
if 'bcca-winter.netlify.app' in final:
    raise SystemExit('Old Netlify domain remains in index.html')
print('Kakao/Open Graph metadata and Carney domain migration complete.')
