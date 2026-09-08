from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

replacements = {
    'BCCA 스쿨링 캠프 14명 모집 마감': 'BCCA 스쿨링 캠프 모집 마감',
    'BCCA 스쿨링 캠프 14명 모집이 마감되었습니다. 추가 자리가 확보되면 이 페이지에서 다시 안내드립니다.': 'BCCA 스쿨링 캠프 모집이 마감되었습니다.(모집 시작 후 26일만에 마감) 추가 자리가 확보되면 이 페이지에서 다시 안내드립니다.',
    'BCCA와 비슷한 비용·구성으로 학교 측 최종 협의 중이며, 확정 전 대기 예약이 가능합니다.': 'BCCA와 비슷한 비용·구성으로 학교 측 최종 협의 중이며, 마감이 빠르므로 확정 전 대기 예약을 추천 드립니다.',
}

for old, new in replacements.items():
    if old not in html:
        raise SystemExit(f'ERROR: target copy not found: {old}')
    html = html.replace(old, new, 1)

for expected in replacements.values():
    if expected not in html:
        raise SystemExit(f'ERROR: replacement missing: {expected}')

path.write_text(html, encoding='utf-8')
print('Updated BCCA recruitment notice copy.')
