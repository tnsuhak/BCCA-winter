from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old_note='''    <p class="note">\n      상담 시 학생의 학년, 현재 영어 수준, 부모님과 떨어져 지낸 경험 여부를 알려주시면 훨씬 정확한 안내가 가능합니다.\n    </p>\n'''
old_footer='''<footer>\n  <div class="wrap">\n    <span><b>TNS유학 · ㈜티앤에스월드와이드</b> · 2027 BCCA 겨울 스쿨링 캠프 안내 페이지</span>\n    <span>서울 02-3288-1733~1735 · 부산 010-5024-1733</span>\n  </div>\n</footer>\n\n'''
if old_note not in s: raise SystemExit('note block not found')
if old_footer not in s: raise SystemExit('footer block not found')
s=s.replace(old_note,'',1).replace(old_footer,'',1)
if '상담 시 학생의 학년, 현재 영어 수준, 부모님과 떨어져 지낸 경험 여부' in s: raise SystemExit('note still present')
if '<footer>' in s and '2027 BCCA 겨울 스쿨링 캠프 안내 페이지' in s: raise SystemExit('duplicate footer still present')
p.write_text(s,encoding='utf-8')
print('Removed duplicate note and footer; sticky bar preserved.')
