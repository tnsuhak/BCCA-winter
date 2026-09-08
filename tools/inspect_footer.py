from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
for term in ['TNS유학 · 해대쉽','강호진 부장','카카오톡 ID','본 페이지는 TNS유학','footer','contact-card']:
    print('\n===',term,'===')
    start=0
    found=0
    while True:
        i=s.find(term,start)
        if i<0 or found>=5: break
        print('POS',i)
        print(s[max(0,i-1200):i+2400].replace('\n','\\n'))
        start=i+len(term); found+=1
