from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Replace the existing five-channel block with the Golden Hills 2+3 card hierarchy.
pattern = re.compile(r'''      <div class="channels">.*?      </div>\n    </div>\n\n    <div class="contact-card reveal">''', re.S)
replacement = '''      <div class="contact-channel-grid" aria-label="TNS유학 상담 및 커뮤니티 채널">
        <div class="contact-channel-primary">
          <a href="https://open.kakao.com/o/slehLvKi" target="_blank" rel="noopener" class="contact-channel-card channel-kakao" aria-label="카카오톡 1대1 상담 열기">
            <span class="channel-icon" aria-hidden="true">💬</span>
            <strong>카톡 상담</strong>
            <small>1:1 실시간 문의</small>
          </a>
          <a href="tel:01051500105" class="contact-channel-card channel-phone" aria-label="전화 상담 010-5150-0105">
            <span class="channel-icon" aria-hidden="true">📞</span>
            <strong>전화 상담</strong>
            <small>010-5150-0105</small>
          </a>
        </div>
        <div class="contact-channel-secondary">
          <a href="https://cafe.naver.com/tnsuhak" target="_blank" rel="noopener" class="contact-channel-card channel-naver" aria-label="네이버 유학카페 열기">
            <span class="channel-icon channel-n" aria-hidden="true">N</span>
            <strong>네이버 유학카페</strong>
            <small>회원 43,000명</small>
          </a>
          <a href="https://open.kakao.com/o/gotTB6re" target="_blank" rel="noopener" class="contact-channel-card channel-canada-room" aria-label="카카오 캐나다 유학정보방 열기">
            <span class="channel-icon" aria-hidden="true">💬</span>
            <strong>카카오 캐나다 유학정보방</strong>
            <small>약 1,300명</small>
          </a>
          <a href="https://tnsuhak.com/" target="_blank" rel="noopener" class="contact-channel-card channel-home" aria-label="TNS유학 홈페이지 열기">
            <span class="channel-icon" aria-hidden="true">🏠</span>
            <strong>TNS유학 홈페이지</strong>
            <small>전체 프로그램 보기</small>
          </a>
        </div>
      </div>
    </div>

    <div class="contact-card reveal">'''

s, count = pattern.subn(replacement, s, count=1)
if count != 1:
    raise SystemExit(f'ERROR: consultation channel block replacement count={count}')

# Remove the older supplemental channel-grid override added earlier.
old_css = '''/* Canada Kakao information room card */
.channels{grid-template-columns:repeat(6,minmax(0,1fr));}
.channels > .ch:nth-child(-n+2){grid-column:span 3;}
.channels > .ch:nth-child(n+3){grid-column:span 2;}
.ch-canada-room{background:#C94A3F;color:#fff;}
.ch-canada-room span{opacity:.82;}
@media(max-width:760px){
  .channels{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;}
  .channels > .ch{grid-column:auto;}
  .channels > .ch:nth-child(5){grid-column:1/-1;}
}

'''
if old_css in s:
    s = s.replace(old_css, '', 1)

# Add Golden Hills-derived card styling, adapted to BCCA variables and the maple-red Canada room.
css_anchor = '/* 2026-09-08 BCCA recruitment closure notice */'
new_css = '''/* TNS consultation cards — Golden Hills 2+3 layout */
.contact-channel-grid{display:grid;gap:16px;margin-top:22px;}
.contact-channel-primary{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;}
.contact-channel-secondary{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;}
.contact-channel-card{min-width:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;border:1px solid #d7dee5;border-radius:16px;padding:18px 14px;box-shadow:0 5px 18px rgba(14,42,71,.06);transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease;}
.contact-channel-primary .contact-channel-card{min-height:154px;}
.contact-channel-secondary .contact-channel-card{min-height:126px;}
.contact-channel-card:hover{transform:translateY(-3px);box-shadow:0 10px 26px rgba(14,42,71,.13);}
.contact-channel-card .channel-icon{font-size:30px;line-height:1;margin-bottom:12px;}
.contact-channel-secondary .channel-icon{font-size:26px;margin-bottom:10px;}
.contact-channel-card strong{display:block;font-size:19px;line-height:1.35;font-weight:800;letter-spacing:-.25px;word-break:keep-all;}
.contact-channel-card small{display:block;margin-top:8px;font-size:13px;line-height:1.45;font-weight:400;word-break:keep-all;}
.channel-kakao{background:#fee500;border-color:#efd800;color:#251d00;}
.channel-kakao small{color:#695b2e;}
.channel-phone{background:#edf3f9;border-color:#c8d3df;color:var(--navy);}
.channel-phone small{color:#657185;}
.channel-naver{background:#03c75a;border-color:#02b351;color:#fff;}
.channel-naver small{color:#dcf8e7;}
.channel-canada-room{background:#C94A3F;border-color:#b83e35;color:#fff;}
.channel-canada-room small{color:rgba(255,255,255,.82);}
.channel-home{background:var(--navy);border-color:var(--navy);color:#fff;}
.channel-home strong{color:#f0d58b;}
.channel-home small{color:#c3ccda;}
.channel-n{width:38px;height:38px;display:flex;align-items:center;justify-content:center;border:2px dotted currentColor;font-family:Arial,sans-serif;font-size:22px!important;font-weight:900;}
@media(max-width:760px){
  .contact-channel-grid{gap:10px;margin-top:16px;}
  .contact-channel-primary,.contact-channel-secondary{gap:10px;}
  .contact-channel-primary .contact-channel-card{min-height:112px;padding:13px 8px;}
  .contact-channel-secondary .contact-channel-card{min-height:96px;padding:11px 6px;}
  .contact-channel-card .channel-icon{font-size:24px;margin-bottom:8px;}
  .contact-channel-secondary .channel-icon{font-size:21px;margin-bottom:7px;}
  .contact-channel-card strong{font-size:15px;}
  .contact-channel-secondary .contact-channel-card strong{font-size:12.5px;line-height:1.35;}
  .contact-channel-card small{font-size:11px;margin-top:5px;}
  .contact-channel-secondary .contact-channel-card small{font-size:9.8px;margin-top:4px;}
  .channel-n{width:27px;height:27px;font-size:15px!important;}
}
@media(max-width:390px){
  .contact-channel-primary,.contact-channel-secondary{gap:8px;}
  .contact-channel-secondary .contact-channel-card{padding-left:5px;padding-right:5px;}
  .contact-channel-secondary .contact-channel-card strong{font-size:12px;}
  .contact-channel-secondary .contact-channel-card small{font-size:9.6px;}
}

'''
if new_css.strip() not in s:
    if css_anchor not in s:
        raise SystemExit('ERROR: CSS insertion anchor not found')
    s = s.replace(css_anchor, new_css + css_anchor, 1)

# Validate required structure and links.
checks = [
    'class="contact-channel-primary"',
    'class="contact-channel-secondary"',
    '카톡 상담',
    '010-5150-0105',
    '네이버 유학카페',
    '카카오 캐나다 유학정보방',
    '약 1,300명',
    'TNS유학 홈페이지',
    'https://open.kakao.com/o/gotTB6re',
]
for x in checks:
    if x not in s:
        raise SystemExit(f'ERROR: missing expected content: {x}')

p.write_text(s, encoding='utf-8')
print('Replaced BCCA consultation cards with Golden Hills-style 2+3 layout.')
