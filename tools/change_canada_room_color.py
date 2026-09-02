from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')
old = '.ch-canada-room{background:#fee500;color:#191919;}'
new = '.ch-canada-room{background:#C94A3F;color:#fff;}'
if old not in html:
    raise SystemExit('ERROR: expected Canada room color rule not found')
html = html.replace(old, new, 1)
path.write_text(html, encoding='utf-8')
print('Updated Canada Kakao info room card to maple red.')
