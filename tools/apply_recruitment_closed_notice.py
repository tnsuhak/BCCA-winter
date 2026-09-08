from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

# Revert the interrupted OG-thumbnail experiment back to the existing production OG image.
preview_og = 'https://deploy-preview-3--bcca-winter.netlify.app/og-bcca-2027.jpg'
production_og = 'https://bcca-winter.netlify.app/og.jpg'
html = html.replace(preview_og, production_og)

# Update the hero CTA so it no longer implies open seats.
html = html.replace('학년별 잔여 정원 문의', '추가 자리·대체 프로그램 문의')

# Mark the current offer as sold out in structured data.
html = html.replace(
    '"availability":"https://schema.org/LimitedAvailability"',
    '"availability":"https://schema.org/SoldOut"'
)

marker = 'BCCA 스쿨링 캠프 14명 모집이 마감되었습니다'
if marker not in html:
    css = r'''
/* 2026-09-08 BCCA recruitment closure notice */
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
    style_close = html.rfind('</style>')
    if style_close == -1:
        raise SystemExit('ERROR: closing </style> not found')
    html = html[:style_close] + css + html[style_close:]

    notice = r'''

<section class="recruitment-notice-wrap" aria-labelledby="recruitment-notice-title">
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
</section>
'''

    h1_pos = html.find('<h1>한국의 겨울방학은')
    if h1_pos == -1:
        raise SystemExit('ERROR: hero H1 anchor not found')
    hero_end = html.find('</section>', h1_pos)
    if hero_end == -1:
        raise SystemExit('ERROR: hero closing section not found')
    hero_end += len('</section>')
    html = html[:hero_end] + notice + html[hero_end:]

required = [
    marker,
    '추가 자리·대체 프로그램 문의',
    'Archbishop Carney Secondary School · 중1~고1',
    'https://schema.org/SoldOut',
    production_og,
    '카카오 캐나다 유학정보방',
]
missing = [x for x in required if x not in html]
if missing:
    raise SystemExit(f'ERROR: missing required content: {missing}')
if preview_og in html:
    raise SystemExit('ERROR: interrupted preview OG URL still present')

path.write_text(html, encoding='utf-8')
print('Applied recruitment closure notice and reverted interrupted OG changes.')
