from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

old_card = '''    <div class="contact-card reveal">
      <h3>TNS유학 · 해대쉽</h3>
      <p class="who">강호진 부장(말랑이) · 유학 전문 경력 18년 · 네이버 유학카페 43,000명 운영</p>
      <div class="lines">
        <a href="tel:01051500105">010-5150-0105</a> &nbsp;|&nbsp; <a href="tel:0232881733">02-3288-1733~5</a><br>
        카카오톡 ID : stardancer &nbsp;|&nbsp; <a href="mailto:khj@tnsuhak.com">khj@tnsuhak.com</a>
      </div>
      <div class="tags">
        <span>#캐나다조기유학</span><span>#밴쿠버유학</span><span>#코퀴틀람유학</span>
        <span>#겨울스쿨링캠프</span><span>#관리형유학</span><span>#BCCA</span><span>#에듀스마트</span>
      </div>
      <p class="disclaimer">
        본 페이지는 TNS유학이 에듀스마트(EduSmart) 2027 겨울 스쿨링 캠프 자료를 바탕으로 정리한 안내 자료입니다.<br>
        비용 · 일정 · 학년 배정은 학년도 및 현지 사정에 따라 변경될 수 있으므로, 신청 시점에 최신 정보를 확인하시기 바랍니다.
      </p>
    </div>'''

new_card = '''    <div class="contact-card reveal">
      <h3>TNS유학 · ㈜티앤에스월드와이드</h3>
      <div class="company-offices">
        <div class="office">
          <b>서울 본사</b>
          <span>서울시 강남구 테헤란로5길 7 KG타워 B1 (06134)</span>
          <a href="tel:0232881733">02-3288-1733~1735</a>
        </div>
        <div class="office">
          <b>부산 지사</b>
          <span>부산 부산진구 중앙대로 694 쥬디스태화 9층 37호 (47295)</span>
          <a href="tel:01050241733">010-5024-1733</a>
        </div>
      </div>
      <div class="tags">
        <span>#캐나다조기유학</span><span>#밴쿠버유학</span><span>#코퀴틀람유학</span>
        <span>#겨울스쿨링캠프</span><span>#관리형유학</span><span>#BCCA</span><span>#에듀스마트</span>
      </div>
      <p class="disclaimer">
        본 페이지는 TNS유학이 에듀스마트(EduSmart) 2027 겨울 스쿨링 캠프 자료를 바탕으로 정리한 안내 자료입니다.<br>
        비용 · 일정 · 학년 배정은 학년도 및 현지 사정에 따라 변경될 수 있으므로, 신청 시점에 최신 정보를 확인하시기 바랍니다.
      </p>
    </div>'''

old_footer = '''<footer>
  <div class="wrap">
    <span><b>TNS유학 (TNS Worldwide)</b> · 2027 BCCA 겨울 스쿨링 캠프 안내 페이지</span>
    <span>khj@tnsuhak.com · 02-3288-1733~5</span>
  </div>
</footer>'''

new_footer = '''<footer>
  <div class="wrap">
    <span><b>TNS유학 · ㈜티앤에스월드와이드</b> · 2027 BCCA 겨울 스쿨링 캠프 안내 페이지</span>
    <span>서울 02-3288-1733~1735 · 부산 010-5024-1733</span>
  </div>
</footer>'''

css_anchor = '''.contact-card .lines a:hover{border-bottom-color:var(--gold);color:var(--gold-light);}
.tags{display:flex;flex-wrap:wrap;justify-content:center;gap:9px;margin:30px 0 0;}'''
css_replacement = '''.contact-card .lines a:hover{border-bottom-color:var(--gold);color:var(--gold-light);}
.company-offices{display:grid;grid-template-columns:1fr 1fr;gap:14px;max-width:900px;margin:24px auto 0;text-align:left;}
.company-offices .office{border:1px solid rgba(255,255,255,.15);border-radius:12px;padding:18px 20px;background:rgba(255,255,255,.035);}
.company-offices .office b{display:block;color:#fff;font-size:15px;margin-bottom:7px;}
.company-offices .office span{display:block;color:#b9cbdb;font-size:13.5px;font-weight:300;line-height:1.6;margin-bottom:7px;}
.company-offices .office a{display:inline-block;color:var(--gold-light);font-size:14.5px;font-weight:600;border-bottom:1px solid rgba(255,255,255,.2);padding-bottom:1px;}
.company-offices .office a:hover{border-bottom-color:var(--gold);}
@media(max-width:760px){
  .contact-card h3{font-size:22px;line-height:1.35;letter-spacing:.01em;}
  .company-offices{grid-template-columns:1fr;gap:10px;margin-top:18px;}
  .company-offices .office{padding:15px 16px;text-align:left;}
  .company-offices .office b{font-size:14px;}
  .company-offices .office span{font-size:12.8px;}
  .company-offices .office a{font-size:13.5px;}
}
.tags{display:flex;flex-wrap:wrap;justify-content:center;gap:9px;margin:30px 0 0;}'''

if old_card not in html:
    raise SystemExit('ERROR: current contact card block not found')
if old_footer not in html:
    raise SystemExit('ERROR: current footer block not found')
if css_anchor not in html:
    raise SystemExit('ERROR: contact CSS anchor not found')

html = html.replace(old_card, new_card, 1)
html = html.replace(old_footer, new_footer, 1)
html = html.replace(css_anchor, css_replacement, 1)

required = [
    'TNS유학 · ㈜티앤에스월드와이드',
    '서울시 강남구 테헤란로5길 7 KG타워 B1 (06134)',
    '02-3288-1733~1735',
    '부산 부산진구 중앙대로 694 쥬디스태화 9층 37호 (47295)',
    '010-5024-1733',
]
for text in required:
    if text not in html:
        raise SystemExit(f'ERROR: missing required corporate detail: {text}')
for obsolete in ['강호진 부장(말랑이)', '카카오톡 ID : stardancer', 'khj@tnsuhak.com', 'TNS유학 · 해대쉽']:
    if obsolete in html:
        raise SystemExit(f'ERROR: obsolete personal footer detail remains: {obsolete}')

path.write_text(html, encoding='utf-8')
print('Updated BCCA contact/company footer to the EduSmart corporate standard.')
