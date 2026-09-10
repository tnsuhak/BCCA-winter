from pathlib import Path
import subprocess,re

path=Path('index.html')
html=path.read_text(encoding='utf-8')
old=subprocess.check_output(['git','show','a340f21d66506ca74d72e3d9467558961dd6e8f8:index.html'],text=True)

# 1) Replace the long HTML schedule table with the supplied brochure-style visual schedule.
new_schedule='''<section id="schedule" class="alt">
  <div class="wrap">
    <div class="s-head">
      <span class="s-num">04 · 5-WEEK SCHEDULE</span>
      <h2>5주 전체 일정,<br>한 장으로 확인하세요</h2>
      <p>미서부 일정부터 Carney 정규 스쿨링, 방과후 ESL·MATH, 홈스테이 활동, UBC 멘토링과 귀국까지 전체 흐름을 한눈에 볼 수 있습니다.</p>
    </div>
    <figure class="schedule-image-card">
      <a href="assets/carney-2027-schedule.svg" target="_blank" rel="noopener" aria-label="2027 Archbishop Carney 겨울 스쿨링 일정표 크게 보기">
        <img src="assets/carney-2027-schedule.svg" alt="2027 Archbishop Carney 겨울 스쿨링 5주 일정표" loading="lazy">
      </a>
      <figcaption>이미지를 누르면 크게 볼 수 있습니다. 상기 일정은 현지 사정에 따라 일부 변경될 수 있습니다.</figcaption>
    </figure>
    <div class="schedule-summary" aria-label="5주 일정 요약">
      <div><b>1주차</b><strong>미서부 5일</strong><span>LA · UCLA · 유니버설 · 디즈니랜드 · 샌디에고</span></div>
      <div><b>2~4주차</b><strong>정규 스쿨링</strong><span>평일 8:30~3:00 Carney 수업 + 홈스테이 이동 + 4:00~5:00 ESL·MATH</span></div>
      <div><b>주말</b><strong>밴쿠버 활동</strong><span>다운타운 · 게스타운 · 스탠리파크 · 메트로타운 · UBC 멘토링</span></div>
      <div><b>5주차</b><strong>수료 · 귀국</strong><span>마지막 수업과 수료식 후 2/13 밴쿠버 출발, 2/14 한국 도착</span></div>
    </div>
  </div>
</section>'''
html,n=re.subn(r'<section id="schedule" class="alt">.*?</section>',new_schedule,html,count=1,flags=re.S)
if n!=1: raise SystemExit('schedule section not found')

# 2) Recover the real Kakao review gallery from the previously approved BCCA production page.
m=re.search(r'<!-- ===== REVIEWS ===== -->\s*(<section id="reviews">.*?</section>)',old,re.S)
if not m: raise SystemExit('old review section not found')
reviews=m.group(1)
reviews=reviews.replace('<span class="s-num">07 &nbsp;REVIEWS</span>','<span class="s-num">11 · PREVIOUS EDUSMART REVIEWS</span>')
reviews=reviews.replace('<h2>다녀온 학생과 학부모님의 기록</h2>','<h2>에듀스마트 겨울 스쿨링<br>실제 카톡 후기</h2>')
reviews=reviews.replace('지난 겨울 캠프에 아이를 보내신 학부모님들이 단톡방에 남겨주신 메시지입니다. 학생 얼굴과 이름은 모두 가렸습니다. 이미지를 누르면 크게 볼 수 있습니다.','아래 후기는 에듀스마트가 운영한 이전 겨울 스쿨링 참가 학부모·학생의 실제 메시지입니다. 2027 Archbishop Carney 참가 후기는 아니며, 학생 얼굴과 이름 등 개인정보는 가렸습니다. 이미지를 누르면 크게 볼 수 있습니다.')
# Add a small context label above gallery if not present.
reviews=reviews.replace('<div class="gal reveal" id="gal">','<div class="review-context"><b>실제 운영 후기</b><span>이전 EduSmart 겨울 스쿨링 참가자 기록 · 개인정보 마스킹</span></div><div class="gal reveal" id="gal">',1)

# Remove any previously restored review block before reinserting.
html=re.sub(r'<section id="reviews">.*?</section>\s*','',html,flags=re.S)
if '<section id="faq">' not in html: raise SystemExit('faq insertion marker not found')
html=html.replace('<section id="faq">',reviews+'\n\n<section id="faq">',1)

# 3) Style schedule visual + reviews.
css='''
/* Brochure-style schedule visual */
.schedule-image-card{margin:0;background:#fff;border:1px solid var(--line);padding:18px;box-shadow:0 12px 34px rgba(14,42,69,.08)}
.schedule-image-card a{display:block;background:#fff;text-align:center}
.schedule-image-card img{display:block;width:100%;max-width:935px;height:auto;margin:0 auto}
.schedule-image-card figcaption{text-align:center;color:var(--muted);font-size:12px;padding:13px 8px 2px}
.schedule-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:16px}
.schedule-summary div{background:#fff;border:1px solid var(--line);padding:18px 16px;min-height:132px}
.schedule-summary b{display:block;color:var(--gold);font-size:11px;letter-spacing:.08em;margin-bottom:5px}
.schedule-summary strong{display:block;font-family:'Gowun Batang',serif;color:var(--navy);font-size:19px;margin-bottom:6px}
.schedule-summary span{display:block;color:#60717f;font-size:11.5px;line-height:1.6}
/* Previous EduSmart Kakao reviews restored from approved BCCA page */
.review-context{display:flex;align-items:center;justify-content:space-between;gap:16px;background:var(--gold-pale);border-left:4px solid var(--gold);padding:14px 16px;margin:-8px 0 22px}
.review-context b{color:var(--navy);font-size:13px}.review-context span{color:#6a727a;font-size:11.5px}
.gal{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.gal-item{background:#fff;border:1px solid var(--line);cursor:zoom-in;transition:.25s;overflow:hidden;display:flex;flex-direction:column;margin:0}
.gal-item:hover{border-color:var(--gold);box-shadow:0 12px 28px rgba(14,42,69,.12);transform:translateY(-3px)}
.gal-item img{width:100%;height:230px;object-fit:cover;object-position:top center;background:#dfe7ef}
.gal-item figcaption{padding:15px 16px 18px;border-top:1px solid var(--line)}
.gal-item strong{display:block;font-size:13px;color:var(--gold);letter-spacing:.02em;margin-bottom:6px;font-weight:600}
.gal-item span{display:block;font-size:14px;color:#41505e;font-weight:300;line-height:1.6}
.gal-more{display:none}.gal.open .gal-more{display:flex}
.gal-toggle{display:block;margin:30px auto 0;background:none;border:1px solid var(--navy);color:var(--navy);font-family:inherit;font-size:14px;font-weight:700;padding:12px 30px;cursor:pointer;transition:.25s}
.gal-toggle:hover{background:var(--navy);color:#fff}
.lb{display:none;position:fixed;inset:0;z-index:300;background:rgba(6,18,30,.93);align-items:center;justify-content:center;padding:56px 20px}
.lb.open{display:flex}.lb img{max-width:min(94vw,560px);max-height:82vh;object-fit:contain;box-shadow:0 24px 60px rgba(0,0,0,.5)}
.lb-close{position:absolute;top:16px;right:20px;background:none;border:0;color:#fff;font-size:38px;line-height:1;cursor:pointer;opacity:.85}
.lb-nav{position:absolute;top:50%;transform:translateY(-50%);background:rgba(255,255,255,.12);border:0;color:#fff;font-size:34px;width:52px;height:64px;cursor:pointer}.lb-nav:hover{background:rgba(255,255,255,.26)}
.lb-prev{left:14px}.lb-next{right:14px}.lb-cap{position:absolute;bottom:18px;left:0;right:0;text-align:center;color:#d5e2ee;font-size:13px;padding:0 24px;font-weight:300}
@media(max-width:900px){.schedule-summary{grid-template-columns:1fr 1fr}.gal{grid-template-columns:repeat(2,1fr)}}
@media(max-width:620px){.schedule-image-card{padding:8px}.schedule-image-card figcaption{font-size:10.5px;line-height:1.55}.schedule-summary{grid-template-columns:1fr 1fr;gap:8px}.schedule-summary div{padding:13px 12px;min-height:116px}.schedule-summary strong{font-size:16px}.schedule-summary span{font-size:10.5px}.review-context{display:block}.review-context span{display:block;margin-top:3px}.gal{grid-template-columns:1fr 1fr;gap:9px}.gal-item img{height:190px}.gal-item figcaption{padding:10px 11px 12px}.gal-item strong{font-size:11px}.gal-item span{font-size:11.5px;line-height:1.5}.lb-nav{width:42px;height:56px}.lb-prev{left:4px}.lb-next{right:4px}}
'''
if '/* Brochure-style schedule visual */' not in html:
    html=html.replace('</style>',css+'\n</style>',1)

# 4) Lightbox + gallery behavior.
lightbox='''<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="후기 이미지 크게 보기">
  <button class="lb-close" id="lbClose" aria-label="닫기">&times;</button>
  <button class="lb-nav lb-prev" id="lbPrev" aria-label="이전 후기">&#8249;</button>
  <img id="lbImg" src="" alt="">
  <button class="lb-nav lb-next" id="lbNext" aria-label="다음 후기">&#8250;</button>
  <div class="lb-cap" id="lbCap"></div>
</div>'''
html=re.sub(r'<div class="lb" id="lb".*?</div>\s*</div>?','',html,flags=re.S)
js='''<script>
(function(){
  var gal=document.getElementById('gal'), toggle=document.getElementById('galToggle');
  if(!gal)return;
  var figs=Array.prototype.slice.call(gal.querySelectorAll('.gal-item'));
  if(toggle){toggle.addEventListener('click',function(){var o=gal.classList.toggle('open');toggle.textContent=o?'접기':'후기 10건 더 보기';});}
  var lb=document.getElementById('lb'), img=document.getElementById('lbImg'), cap=document.getElementById('lbCap'), cur=0;
  function show(i){if(!figs.length)return;if(i<0)i=figs.length-1;if(i>=figs.length)i=0;cur=i;var f=figs[i],im=f.querySelector('img'),s=f.querySelector('strong'),t=f.querySelector('span');img.src=im.src;img.alt=im.alt||'';cap.textContent=(s?s.textContent:'')+(t?' — '+t.textContent:'');}
  function open(i){show(i);lb.classList.add('open');document.body.style.overflow='hidden';}
  function close(){lb.classList.remove('open');document.body.style.overflow='';}
  figs.forEach(function(f,i){f.addEventListener('click',function(){open(i);});});
  document.getElementById('lbClose').addEventListener('click',close);document.getElementById('lbPrev').addEventListener('click',function(){show(cur-1)});document.getElementById('lbNext').addEventListener('click',function(){show(cur+1)});
  lb.addEventListener('click',function(e){if(e.target===lb)close();});document.addEventListener('keydown',function(e){if(!lb.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1);});
})();
</script>'''
if 'id="lb" role="dialog"' not in html:
    html=html.replace('</body>',lightbox+'\n'+js+'\n</body>',1)

# Add reviews to desktop nav if practical.
html=html.replace('<a href="#faq">FAQ</a>','<a href="#reviews">후기</a><a href="#faq">FAQ</a>',1)

# Public-content safeguards.
for forbidden in ['에이전트 커미션','CAD $1,500','강수정 차장','Kim Jihoon / 1-778']:
    if forbidden in html: raise SystemExit('forbidden internal text leaked: '+forbidden)
if '2027 Archbishop Carney 참가 후기는 아니며' not in html: raise SystemExit('review context disclaimer missing')
if 'assets/carney-2027-schedule.svg' not in html: raise SystemExit('schedule image missing')
if len(re.findall(r'class="gal-item',html)) < 10: raise SystemExit('review images not restored')

path.write_text(html,encoding='utf-8')
print('Schedule visual installed and previous EduSmart Kakao reviews restored:',len(re.findall(r'class="gal-item',html)),'items')
