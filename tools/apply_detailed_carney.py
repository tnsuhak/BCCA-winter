from pathlib import Path
import base64
import gzip

payload = ''.join(
    Path(f'tools/carney_payload/part{i}.txt').read_text(encoding='utf-8').strip()
    for i in range(1, 5)
)
# One character was dropped while the first payload chunk was transferred.
# Restore that exact character before decoding, then validate the final page.
payload = payload.replace('VK4vl141bZD', 'VK4vlV141bZD', 1)
html = gzip.decompress(base64.b64decode(payload)).decode('utf-8')

required = [
    '2027 Carney 겨울 스쿨링',
    '5주 일정은',
    '학생에게 실제로',
    '정규수업 70~80%',
    'US$500 + CA$500',
    '실제 학생생활 영상 11개 전체 보기',
    '카카오 캐나다 유학정보방',
]
for item in required:
    if item not in html:
        raise SystemExit(f'missing required detail: {item}')

for forbidden in [
    '에이전트 커미션', '한국 계좌', '캐나다 계좌', 'CAD $1,500',
    '강수정 차장', '778-928-9303'
]:
    if forbidden in html:
        raise SystemExit(f'forbidden private detail present: {forbidden}')

Path('index.html').write_text(html, encoding='utf-8')
print('Detailed Carney page written:', len(html))
