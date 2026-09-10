from pathlib import Path
import re, base64, io, urllib.request
from PIL import Image

html=Path('index.html').read_text(encoding='utf-8')
seen=set(); items=[]

def add(src,pos,kind):
    src=src.strip().strip('"\'')
    if not src or src in seen: return
    seen.add(src)
    context=re.sub(r'\s+',' ',html[max(0,pos-220):min(len(html),pos+420)])
    items.append((kind,src,context[:550]))

for m in re.finditer(r'<img\b[^>]*>',html,re.I|re.S):
    sm=re.search(r'\bsrc\s*=\s*(["\'])(.*?)\1',m.group(0),re.I|re.S)
    if sm: add(sm.group(2),m.start(),'img')
for m in re.finditer(r'url\(\s*(["\']?)(.*?)\1\s*\)',html,re.I|re.S):
    add(m.group(2),m.start(),'css-url')
for m in re.finditer(r'https?://[^"\'\s)]+\.(?:jpe?g|png|webp)(?:\?[^"\'\s)]*)?',html,re.I):
    add(m.group(0),m.start(),'absolute')

def inspect(src):
    try:
        if src.startswith('data:image/'):
            if ';base64,' not in src:return 'data(non-base64)'
            data=base64.b64decode(re.sub(r'\s+','',src.split(';base64,',1)[1]),validate=False)
        elif src.startswith('http'):
            req=urllib.request.Request(src,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=12) as r:data=r.read(12_000_000)
        else:
            p=Path(src.split('?',1)[0].lstrip('/'))
            if not p.exists():return 'missing-local'
            data=p.read_bytes()
        im=Image.open(io.BytesIO(data)); return f'{im.size[0]}x{im.size[1]} {im.format}'
    except Exception as e:return 'ERR '+str(e)[:100]

print('TOTAL',len(items))
for i,(kind,src,ctx) in enumerate(items[:60],1):
    shown = '[data-image]' if src.startswith('data:image/') else src[:240]
    print(f'[{i}] {kind} {inspect(src)} :: {shown}')
    print('CTX:',ctx.replace('\n',' ')[:550])
