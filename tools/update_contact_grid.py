from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

replacements = [
    (
        ".channels{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}",
        ".channels{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;}"
    ),
    (
        ".ch-kakao{background:#fae100;color:#3c1e1e;}\n.ch-cafe{background:#03c75a;color:#fff;}\n.ch-home{background:var(--navy);color:#fff;}\n.ch-home span,.ch-cafe span{opacity:.85;}",
        ".ch-kakao{background:#fae100;color:#3c1e1e;}\n.ch-phone{background:#fff;color:var(--navy);border:1px solid #d8c98e;}\n.ch-cafe{background:#03c75a;color:#fff;}\n.ch-home{background:var(--navy);color:#fff;}\n.ch-home span,.ch-cafe span,.ch-phone span{opacity:.85;}"
    ),
    (
        ".grid3,.grid2,.channels{grid-template-columns:1fr;}",
        ".grid3,.grid2{grid-template-columns:1fr;}\n  .channels{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;}"
    ),
    (
'''        <a class="ch ch-kakao" href="https://open.kakao.com/me/tnsuhak" target="_blank" rel="noopener">
          <span class="ic">💬</span><b>카톡 상담</b><span>1:1 실시간 문의</span>
        </a>
        <a class="ch ch-cafe" href="https://cafe.naver.com/tnsuhak" target="_blank" rel="noopener">
          <span class="ic">N</span><b>네이버 유학카페</b><span>회원 43,000명</span>
        </a>
        <a class="ch ch-home" href="https://tnsuhak.com/" target="_blank" rel="noopener">
          <span class="ic">🏠</span><b>TNS유학 홈페이지</b><span>전체 프로그램 보기</span>
        </a>''',
'''        <a class="ch ch-kakao" href="https://open.kakao.com/me/tnsuhak" target="_blank" rel="noopener">
          <span class="ic">💬</span><b>카톡 상담</b><span>1:1 실시간 문의</span>
        </a>
        <a class="ch ch-phone" href="tel:01051500105">
          <span class="ic">☎</span><b>전화상담</b><span>010-5150-0105</span>
        </a>
        <a class="ch ch-cafe" href="https://cafe.naver.com/tnsuhak" target="_blank" rel="noopener">
          <span class="ic">N</span><b>네이버 유학카페</b><span>회원 43,000명</span>
        </a>
        <a class="ch ch-home" href="https://tnsuhak.com/" target="_blank" rel="noopener">
          <span class="ic">🏠</span><b>TNS유학 홈페이지</b><span>전체 프로그램 보기</span>
        </a>'''
    ),
]

for old, new in replacements:
    if old not in html:
        raise SystemExit(f"Expected block not found: {old[:100]}")
    html = html.replace(old, new, 1)

path.write_text(html, encoding="utf-8")
print("Updated contact area to a 2x2 grid with phone consultation.")
