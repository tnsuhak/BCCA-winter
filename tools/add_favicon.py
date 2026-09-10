from pathlib import Path
import re

TAG = '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
for name in ('index.html','student-life-videos.html'):
    p=Path(name)
    if not p.exists():
        continue
    s=p.read_text(encoding='utf-8')
    if 'href="/favicon.svg"' not in s and "href='/favicon.svg'" not in s:
        m=re.search(r'<head\b[^>]*>',s,re.I)
        if not m:
            raise SystemExit(f'No head in {name}')
        s=s[:m.end()]+'\n'+TAG+s[m.end():]
        p.write_text(s,encoding='utf-8')
        print('updated',name)
    else:
        print('already',name)
