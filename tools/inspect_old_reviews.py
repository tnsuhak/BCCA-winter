from pathlib import Path
import subprocess,re
old=subprocess.check_output(['git','show','a340f21d66506ca74d72e3d9467558961dd6e8f8:index.html'],text=True)
terms=['후기','카톡','카카오','review','testimonial','학부모']
for term in terms:
    print('\n====',term,'====')
    for m in list(re.finditer(term,old,re.I))[:12]:
        a=max(0,m.start()-1800); b=min(len(old),m.end()+3500)
        chunk=old[a:b]
        # Avoid dumping giant base64 payloads
        chunk=re.sub(r'data:image/[^;]+;base64,[A-Za-z0-9+/=]{200,}', 'DATA_IMAGE_REDACTED', chunk)
        print('POS',m.start())
        print(chunk)
