from pathlib import Path
import subprocess,re
old=subprocess.check_output(['git','show','a340f21d66506ca74d72e3d9467558961dd6e8f8:index.html'],text=True)
current=Path('index.html').read_text(encoding='utf-8')
print('CURRENT SECTIONS:')
for tag in re.findall(r'<section[^>]*>', current): print(tag)
print('\nCURRENT SPECIAL MARKERS:')
for term in ['TNS CONSULTATION','FAQ','실제 학생','상담']:
    print(term, current.find(term))
print('\nOLD REVIEWS MARKERS:')
for term in ['<!-- ===== REVIEWS ===== -->','<section id="reviews">','<div class="lb" id="lb"']:
    print(term, old.find(term))
