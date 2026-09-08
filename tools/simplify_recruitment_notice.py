from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

old_css = '''/* 2026-09-08 BCCA recruitment closure notice */
.recruitment-notice-wrap{padding:28px 0 12px;}
.recruitment-notice{
  background:#fff;border:1px solid rgba(201,74,63,.28);border-left:5px solid #C94A3F;
  border-radius:16px;padding:28px 30px;box-shadow:0 10px 30px rgba(14,42,71,.07);
}
.rn-top{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px;}
.rn-badge{display:inline-flex;align-items:center;background:#C94A3F;color:#fff;border-radius:999px;padding:7px 12px;font-size:13px;font-weight:700;}
.rn-date{color:var(--muted);font-size:12.5px;}
.recruitment-notice h2{font-family:'Gowun Batang',serif;color:var(--navy);font-size:clamp(22px,3vw,30px);line-height:1.35;margin:0 0 10px;}
.recruitment-notice > p{color:var(--muted);font-size:15px;line-height:1.75;margin:0;}
.rn-alt{margin-top:20px;padding-top:20px;border-top:1px solid #ece6d9;}
.rn-alt strong{display:block;color:var(--navy);font-size:17px;margin-bottom:5px;}
.rn-alt .rn-school{display:block;color:#C94A3F;font-weight:700;font-size:15px;margin-bottom:8px;}
.rn-alt p{color:var(--muted);font-size:14px;line-height:1.7;margin:0 0 14px;}
.rn-alt a{display:inline-flex;align-items:center;justify-content:center;background:var(--navy);color:#fff;border-radius:10px;padding:11px 16px;font-size:14px;font-weight:700;}
@media(max-width:760px){
  .recruitment-notice-wrap{padding:18px 0 6px;}
  .recruitment-notice{padding:22px 18px;}
  .rn-top{align-items:flex-start;flex-direction:column;gap:7px;}
}
'''

new_css = '''/* 2026-09-08 BCCA recruitment closure notice */
.recruitment-notice-wrap{padding:22px 0 16px;}
.recruitment-notice{
  background:#fff;border:1px solid rgba(201,74,63,.24);border-left:4px solid #C94A3F;
  border-radius:14px;padding:24px 26px;box-shadow:0 8px 24px rgba(14,42,71,.06);
}
.rn-top{margin-bottom:10px;}
.rn-badge{display:inline-flex;align-items:center;background:#C94A3F;color:#fff;border-radius:999px;padding:6px 10px;font-size:12px;font-weight:700;}
.recruitment-notice h2{font-family:'Gowun Batang',serif;color:var(--navy);font-size:clamp(21px,2.4vw,27px);line-height:1.35;margin:0 0 8px;}
.recruitment-notice > p{color:var(--muted);font-size:14.5px;line-height:1.65;margin:0;}
.rn-alt{margin-top:16px;padding-top:16px;border-top:1px solid #ece6d9;}
.rn-alt strong{display:block;color:var(--navy);font-size:16px;margin-bottom:4px;}
.rn-alt .rn-school{display:block;color:#B94A40;font-weight:600;font-size:13.5px;line-height:1.5;margin-bottom:6px;}
.rn-alt p{color:var(--muted);font-size:13.8px;line-height:1.6;margin:0 0 12px;}
.rn-alt a{display:inline-flex;align-items:center;justify-content:center;background:var(--navy);color:#fff;border-radius:9px;padding:10px 14px;font-size:13.5px;font-weight:700;}
@media(max-width:760px){
  .recruitment-notice-wrap{padding:14px 0 8px;}
  .recruitment-notice{padding:18px 16px;border-radius:12px;}
  .recruitment-notice h2{font-size:22px;line-height:1.32;margin-bottom:7px;}
  .recruitment-notice > p{font-size:14.5px;line-height:1.6;}
  .rn-alt{margin-top:14px;padding-top:14px;}
  .rn-alt strong{font-size:15.5px;}
  .rn-alt .rn-school{font-size:13px;}
  .rn-alt p{font-size:13.5px;line-height:1.58;}
}
'''

old_html = '''<section class="recruitment-notice-wrap" aria-labelledby="recruitment-notice-title">
  <div class="container">
    <div class="recruitment-notice">
      <div class="rn-top">
        <span class="rn-badge">모집 마감 안내</span>
        <span class="rn-date">2026. 9. 8 업데이트</span>
      </div>
      <h2 id="recruitment-notice-title">BCCA 스쿨링 캠프 14명 모집이 마감되었습니다</h2>
      <p>현재 안내된 BCCA 스쿨링 캠프 14명 모집은 최종 마감되었습니다. 추후 BCCA에서 추가 자리가 확보될 경우 이 페이지에서 다시 안내드리겠습니다.</p>
      <div class="rn-alt">
        <strong>대체 스쿨링 프로그램 준비 중</strong>
        <span class="rn-school">Archbishop Carney Secondary School · 중1~고1</span>
        <p>BCCA와 동일한 수준의 비용과 구성으로 준비 중이며, 현재 학교 측 최종 컨펌을 진행하고 있습니다. 확정되는 대로 세부 일정을 안내드리며, 관심 있는 학생은 미리 대기 예약을 신청할 수 있습니다.</p>
        <a href="#inquiry">대기 예약 문의</a>
      </div>
    </div>
  </div>
</section>'''

new_html = '''<section class="recruitment-notice-wrap" aria-labelledby="recruitment-notice-title">
  <div class="container">
    <div class="recruitment-notice">
      <div class="rn-top"><span class="rn-badge">모집 마감</span></div>
      <h2 id="recruitment-notice-title">BCCA 스쿨링 캠프 14명 모집 마감</h2>
      <p>BCCA 스쿨링 캠프 14명 모집이 마감되었습니다. 추가 자리가 확보되면 이 페이지에서 다시 안내드립니다.</p>
      <div class="rn-alt">
        <strong>대체 프로그램 준비 중</strong>
        <span class="rn-school">Archbishop Carney Secondary School · 중1~고1</span>
        <p>BCCA와 비슷한 비용·구성으로 학교 측 최종 협의 중이며, 확정 전 대기 예약이 가능합니다.</p>
        <a href="#inquiry">대기 예약 문의</a>
      </div>
    </div>
  </div>
</section>'''

if old_css not in html:
    raise SystemExit('ERROR: expected notice CSS block not found')
if old_html not in html:
    raise SystemExit('ERROR: expected notice HTML block not found')

html = html.replace(old_css, new_css, 1)
html = html.replace(old_html, new_html, 1)

checks = [
    'BCCA 스쿨링 캠프 14명 모집 마감',
    '추가 자리가 확보되면 이 페이지에서 다시 안내드립니다.',
    '대체 프로그램 준비 중',
    'Archbishop Carney Secondary School · 중1~고1',
]
missing = [x for x in checks if x not in html]
if missing:
    raise SystemExit(f'ERROR: missing expected simplified content: {missing}')
if '2026. 9. 8 업데이트' in html:
    raise SystemExit('ERROR: visible update date remains in notice')

path.write_text(html, encoding='utf-8')
print('Simplified recruitment notice content and typography.')
