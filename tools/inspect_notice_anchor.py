from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
for term in ['D-54','잔금','PROGRAM','Program','program','01']:
    print('\n===',term,'===')
    start=0
    found=0
    while True:
        i=s.find(term,start)
        if i<0 or found>=10: break
        print('POS',i)
        print(s[max(0,i-500):i+800].replace('\n','\\n'))
        start=i+len(term); found+=1
