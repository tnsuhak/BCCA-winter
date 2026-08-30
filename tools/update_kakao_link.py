from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")
old = 'https://open.kakao.com/me/tnsuhak'
new = 'https://open.kakao.com/o/slehLvKi'
if old not in html:
    raise SystemExit('Old Kakao URL not found')
html = html.replace(old, new, 1)
path.write_text(html, encoding="utf-8")
print('Updated Kakao consultation link.')
