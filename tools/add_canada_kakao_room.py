from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')

ROOM_URL = 'https://open.kakao.com/o/gotTB6re'
if ROOM_URL in html:
    print('Canada Kakao info room already present; no change needed.')
    raise SystemExit(0)

# Find the existing Naver cafe card and insert the Canada Kakao room immediately after it.
anchor_re = re.compile(r'<a\b[^>]*>.*?</a>', re.S | re.I)
naver_match = None
for match in anchor_re.finditer(html):
    block = match.group(0)
    if '네이버 유학카페' in block:
        naver_match = match
        break

if not naver_match:
    raise SystemExit('ERROR: Could not find the Naver study-abroad cafe card.')

new_card = '''\n        <a class="ch ch-canada-room" href="https://open.kakao.com/o/gotTB6re" target="_blank" rel="noopener">\n          <span class="ic">💬</span><b>카카오 캐나다 유학정보방</b><span>약 1,300명</span>\n        </a>'''

insert_at = naver_match.end()
html = html[:insert_at] + new_card + html[insert_at:]

# Add layout overrides at the end of the existing stylesheet so the top row stays 2 cards
# and the lower row becomes Naver / Canada Kakao room / TNS in 3 equal cards.
css = '''\n/* Canada Kakao information room card */\n.channels{grid-template-columns:repeat(6,minmax(0,1fr));}\n.channels > .ch:nth-child(-n+2){grid-column:span 3;}\n.channels > .ch:nth-child(n+3){grid-column:span 2;}\n.ch-canada-room{background:#fee500;color:#191919;}\n.ch-canada-room span{opacity:.82;}\n@media(max-width:760px){\n  .channels{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;}\n  .channels > .ch{grid-column:auto;}\n  .channels > .ch:nth-child(5){grid-column:1/-1;}\n}\n'''

style_close = html.rfind('</style>')
if style_close == -1:
    raise SystemExit('ERROR: Could not find closing </style> tag.')
html = html[:style_close] + css + html[style_close:]

# Safety checks.
checks = [
    ('new URL', ROOM_URL),
    ('new label', '카카오 캐나다 유학정보방'),
    ('member count', '약 1,300명'),
    ('Naver card preserved', '네이버 유학카페'),
    ('TNS card preserved', 'TNS유학 홈페이지'),
    ('phone preserved', '010-5150-0105'),
]
for label, needle in checks:
    if needle not in html:
        raise SystemExit(f'ERROR: validation failed: {label}')

path.write_text(html, encoding='utf-8')
print('Added Canada Kakao info room card and responsive layout overrides.')
